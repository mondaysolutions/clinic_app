from flask_appbuilder import ModelView, BaseView
from flask_appbuilder.urltools import *
from flask_appbuilder.actions import action
from flask_appbuilder.baseviews import expose
from flask_appbuilder.security.decorators import has_access

from flask import abort, Blueprint, flash, render_template, request, session, url_for, redirect, request


class AuditModelView(ModelView):
    pk = None
    parent_datamodel_name = None

    list_template = 'general/model/list.html'
    order_columns = ['id']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by', 'changed_on', 'status']
    show_exclude_columns = ['created_by', 'created_on', 'changed_by', 'changed_on', 'status']
    add_exclude_columns = ['created_by', 'created_on', 'changed_by', 'changed_on', 'status']
    search_exclude_columns = ['created_by', 'created_on', 'changed_by', 'changed_on', 'status']
    page_size = 100000

    def _get_list_widget(
            self,
            filters,
            actions=None,
            order_column="",
            order_direction="",
            page=None,
            page_size=None,
            widgets=None,
            **args):

        """ get joined base filter and current active filter for query """
        widgets = widgets or {}
        actions = actions or self.actions
        page_size = page_size or self.page_size
        if not order_column and self.base_order:
            order_column, order_direction = self.base_order
        joined_filters = filters.get_joined_filters(self._base_filters)
        count, lst = self.datamodel.query(
            joined_filters,
            order_column,
            order_direction,
            page=page,
            page_size=page_size,
        )
        pks = self.datamodel.get_keys(lst)

        # serialize composite pks
        pks = [self._serialize_pk_if_composite(pk) for pk in pks]

        widgets["list"] = self.list_widget(
            label_columns=self.label_columns,
            include_columns=self.list_columns,
            value_columns=self.datamodel.get_values(lst, self.list_columns),
            order_columns=self.order_columns,
            formatters_columns=self.formatters_columns,
            page=page,
            page_size=page_size,
            count=count,
            pks=pks,
            actions=actions,
            filters=filters,
            modelview_name=self.__class__.__name__,
        )
        return widgets

    def _list(self):
        """
            list function logic, override to implement different logic
            returns list and search widget
        """
        if get_order_args().get(self.__class__.__name__):
            order_column, order_direction = get_order_args().get(self.__class__.__name__)
        else:
            order_column, order_direction = '', ''
        page = get_page_args().get(self.__class__.__name__)
        page_size = get_page_size_args().get(self.__class__.__name__)
        get_filter_args(self._filters)
        widgets = self._get_list_widget(filters=self._filters,
                                        order_column=order_column,
                                        order_direction=order_direction,
                                        page=None,
                                        page_size=None)
        form = self.search_form.refresh()
        self.update_redirect()
        return self._get_search_widget(form=form, widgets=widgets)

    def _add(self):
        """
            Add function logic, override to implement different logic
            returns add widget or None
        """
        is_valid_form = True
        get_filter_args(self._filters)
        exclude_cols = self._filters.get_relation_cols()
        form = self.add_form.refresh()
        self.url = request.url

        if request.method == "POST":
            self._fill_form_exclude_cols(exclude_cols, form)
            if form.validate():
                self.process_form(form, True)
                item = self.datamodel.obj()
                form.populate_obj(item)

                try:
                    self.pre_add(item)
                except Exception as e:
                    flash(str(e), "danger")
                else:
                    try:
                        if self.datamodel.add(item):
                            self.post_add(item)
                            self.pk = self.datamodel.get_pk_value(item)
                        flash(*self.datamodel.message)
                    except Exception as e:
                        print(str(e))
                finally:
                    return None
            else:
                is_valid_form = False
        if is_valid_form:
            self.update_redirect()
        return self._get_add_widget(form=form, exclude_cols=exclude_cols)

    def _edit(self, pk):
        """
            Edit function logic, override to implement different logic
            returns Edit widget and related list or None
        """
        is_valid_form = True
        pages = get_page_args()
        page_sizes = get_page_size_args()
        orders = get_order_args()
        get_filter_args(self._filters)
        exclude_cols = self._filters.get_relation_cols()

        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        # convert pk to correct type, if pk is non string type.
        pk = self.datamodel.get_pk_value(item)
        self.pk = pk
        self.url = request.url

        if request.method == "POST":
            form = self.edit_form.refresh(request.form)
            # fill the form with the suppressed cols, generated from exclude_cols
            self._fill_form_exclude_cols(exclude_cols, form)
            # trick to pass unique validation
            form._id = pk
            if form.validate():
                self.process_form(form, False)
                form.populate_obj(item)
                try:
                    self.pre_update(item)
                except Exception as e:
                    flash(str(e), "danger")
                else:
                    if self.datamodel.edit(item):
                        self.post_update(item)
                    flash(*self.datamodel.message)
                finally:
                    return None
            else:
                is_valid_form = False
        else:
            # Only force form refresh for select cascade events
            form = self.edit_form.refresh(obj=item)
            # Perform additional actions to pre-fill the edit form.
            self.prefill_form(form, pk)

        widgets = self._get_edit_widget(pk=pk, form=form, exclude_cols=exclude_cols)
        widgets = self._get_related_views_widgets(
            item,
            filters={},
            orders=orders,
            pages=pages,
            page_sizes=page_sizes,
            widgets=widgets,
        )
        if is_valid_form:
            self.update_redirect()
        return widgets

    def _delete(self, pk):
        """
            Delete function logic, override to implement different logic
            deletes the record with primary_key = pk

            :param pk:
                record primary key to delete
        """
        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        try:
            self.pre_delete(item)
        except Exception as e:
            flash(str(e), "danger")
        else:
            if self.datamodel.delete(item):
                self.post_delete(item)
            flash(*self.datamodel.message)
            self.update_redirect()

    def post_add_redirect(self):
        """Override this function to control the
        redirect after add endpoint is called."""
        return redirect(self.get_redirect())

    def post_edit_redirect(self):
        """Override this function to control the
        redirect after edit endpoint is called."""
        return redirect(self.get_redirect())


    # # @has_access
    # @action("return_to_list", "Return to List", "", "fa-list", btnclass="btn-info", multiple=False)
    # def return_to_list(self, item):
    #     # current_date = datetime.now().strftime("%Y-%m-%d")
    #     return redirect('/{}/list'.format(self.__class__.__name__.lower()))

    """
    --------------------------------
            LIST
    --------------------------------
    """
    @expose('/list/')
    @has_access
    def list(self):
        widgets = self._list()
        return self.render_template(self.list_template,
                                    title=self.list_title,
                                    widgets=widgets)

    """
    --------------------------------
            SHOW
    --------------------------------
    """

    @expose("/show/<pk>", methods=["GET"])
    @has_access
    def show(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        widgets = self._show(pk)
        return self.render_template(
            self.show_template,
            pk=pk,
            title=self.show_title,
            widgets=widgets,
            related_views=self._related_views,
        )

    """
    ---------------------------
            ADD
    ---------------------------
    """

    @expose("/add", methods=["GET", "POST"])
    @has_access
    def add(self):
        widget = self._add()
        if not widget:
            return self.post_add_redirect()
        else:
            return self.render_template(
                self.add_template, title=self.add_title, widgets=widget
            )

    """
    ---------------------------
            EDIT
    ---------------------------
    """

    @expose("/edit/<pk>", methods=["GET", "POST"])
    @has_access
    def edit(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        widgets = self._edit(pk)
        if not widgets:
            return self.post_edit_redirect()
        else:
            return self.render_template(
                self.edit_template,
                title=self.edit_title,
                widgets=widgets,
                related_views=self._related_views,
            )

    """
    ---------------------------
            DELETE
    ---------------------------
    """

    @expose("/delete/<pk>")
    @has_access
    def delete(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        self._delete(pk)
        return self.post_delete_redirect()

