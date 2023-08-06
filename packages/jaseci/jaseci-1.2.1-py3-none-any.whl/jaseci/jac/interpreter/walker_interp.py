"""
Walker interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.graph.node import node
from jaseci.jac.interpreter.interp import interp
from jaseci.jac.jac_set import jac_set
from jaseci.jac.machine.jac_scope import jac_scope


class walker_interp(interp):
    """Jac interpreter mixin for objects that will execute Jac code"""
    # Walker only executes statements, sentinels handle attr_stmts

    def run_walker(self, jac_ast):
        """
        walker:
            KW_WALKER NAME namespace_list LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        self.push_scope(
            jac_scope(
                parent=self,
                has_obj=self,
                action_sets=[self.activity_action_ids,
                             self.current_node.activity_action_ids]))
        self._jac_scope.set_live_var(
            'here', self.current_node.id.urn, [], jac_ast)

        self.trigger_entry_actions()
        kid = jac_ast.kid

        if(self.current_step == 0):
            for i in kid:
                if(i.name == 'attr_stmt'):
                    self.run_attr_stmt(jac_ast=i, obj=self)
        for i in kid:
            if(i.name == 'walk_entry_block'):
                self.run_walk_entry_block(i)
            if(i.name == 'statement'):
                self.run_statement(i)
            if(i.name == 'walk_activity_block'):
                self.run_walk_activity_block(i)
            if(i.name == 'walk_exit_block'):
                self.run_walk_exit_block(i)

        # self.trigger_activity_actions()
        self.trigger_exit_actions()
        self.pop_scope()

    def run_walk_entry_block(self, jac_ast):
        """
        walk_entry_block: KW_WITH KW_ENTRY code_block;
        """
        kid = jac_ast.kid
        if (self.current_step == 0):
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_exit_block(self, jac_ast):
        """
        walk_exit_block: KW_WITH KW_EXIT code_block;
        """
        kid = jac_ast.kid
        self._stopped = None
        if (len(self.next_node_ids) == 0):
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_activity_block(self, jac_ast):
        """
        walk_activity_block: KW_WITH KW_ACTIVITY code_block;
        """
        kid = jac_ast.kid
        self.run_code_block(kid[2])

    def run_walker_action(self, jac_ast):
        """
        walker_action:
            ignore_action
            | take_action
            | destroy_action
            | KW_DISENGAGE SEMI;
        """
        kid = jac_ast.kid
        if (kid[0].name == 'KW_DISENGAGE'):
            self._stopped = 'stop'
            self.next_node_ids.remove_all()
        else:
            expr_func = getattr(self, f'run_{kid[0].name}')
            expr_func(kid[0])

    def run_ignore_action(self, jac_ast):
        """
        ignore_action: KW_IGNORE expression SEMI;
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        if (isinstance(result, node)):
            self.ignore_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            self.ignore_node_ids += result
        else:
            self.rt_error(f'{result} is not ignorable type (i.e., nodes)',
                          kid[1])

    def run_take_action(self, jac_ast):
        """
        take_action:
            KW_TAKE expression (SEMI | else_stmt);
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        before = len(self.next_node_ids)
        if (isinstance(result, node)):
            self.next_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            self.next_node_ids += result
        elif(result):
            self.rt_error(f'{result} is not destination type (i.e., nodes)',
                          kid[1])
        after = len(self.next_node_ids)
        if (before >= after and kid[2].name == 'else_stmt'):
            self.run_else_stmt(kid[2])
        after = len(self.next_node_ids)
        # if(before >= after and not self.stopped == 'stop'):
        #     self.rt_info(f"Walker was unable to take any edge" +
        #                  f" - {self.current_node}", kid[0])

    def run_destroy_action(self, jac_ast):
        """
        destroy_action: KW_DESTROY expression SEMI;
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        if (isinstance(result, node)):
            self.destroy_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            self.destroy_node_ids += result
        else:
            self.rt_error(f'{result} is not destroyable type (i.e., nodes)',
                          kid[1])

    # Helper Functions ##################

    def trigger_entry_actions(self):
        """Trigger current node actions on entry"""
        for i in self.current_node.entry_action_ids.obj_list():
            i.trigger()

    def trigger_activity_actions(self):
        """Trigger current node actions on activity"""
        for i in self.current_node.activity_action_ids.obj_list():
            i.trigger()

    def trigger_exit_actions(self):
        """Trigger current node actions on exit"""
        for i in self.current_node.exit_action_ids.obj_list():
            i.trigger()

    def viable_nodes(self):
        """Returns all nodes that shouldnt be ignored"""
        ret = jac_set(self)
        for i in self.current_node.attached_nodes():
            if (i not in self.ignore_node_ids.obj_list()):
                ret.add_obj(i)
        return ret
