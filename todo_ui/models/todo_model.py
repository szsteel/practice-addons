# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Tag(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'
    _parent_store = True
    name = fields.Char('Name', size=40, translate=True)
    parent_id = fields.Many2one(
        'todo.task.tag', 'Parent Tag', ondelete='restrict'
    )
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')
    # Tag class relationship to Tasks;
    task_ids = fields.Many2many('todo.task', string='Tasks')

class Stage(models.Model):
    _name = 'todo.task.stage'
    _description = 'To-do Stage'
    _order = 'sequence,name'
    # String fields
    name = fields.Char('Name', size=40, translate=True)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft','New'),('open','Started'),('done','Closed')],'State'
    )
    docs = fields.Html('Documentation')
    # Numeric fields
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3, 2))
    # Date fields
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')
    # Other fields
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    # Stage class relationship to Tasks;
    task_ids = fields.One2many('todo.task', 'stage_id', string='Tasks in this stage')

class TodoTask(models.Model):
    _inherit = 'todo.task'
    _sql_constraints = [
        ('todo_task_name_uniq',
         'UNIQUE (name, active)',
         'Task title must be unique!')
    ]
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    refers_to = fields.Reference(
        [('res.user', 'User'), ('res.partner', 'Partner')], 'Refers to'
    )
    stage_fold = fields.Boolean(
        string = 'Stage Folded?',
        compute='_compute_stage_fold',
        # store=False  # the default
        search='_search_stage_fold',
        inverse='_write_stage_fold'
    )
    stage_state = fields.Selection(
        related = 'stage_id.state',
        string = 'Stage State'
    )
    user_todo_count = fields.Integer(
        'User To-Do Count',
        compute = '_compute_user_todo_count'
    )

    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name) < 5:
                raise ValidationError('Must have 5 chars!')

    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for task in self:
            task.stage_fold = task.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    def _compute_user_todo_count(self):
        for task in self:
            task.user_todo_count = task.search_count(
                [('user_id', '=', task.user_id.id)]
            )