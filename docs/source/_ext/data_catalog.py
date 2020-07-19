from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst import Directive
import yaml
import json
import os

class CustomDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)

class DataCatalog(Directive):

    optional_arguments = 2

    has_content = True

    option_spec = {
        'source': directives.unchanged,
        'name': directives.unchanged
    }

    @staticmethod
    def load_yaml(path):

        with open(path) as file:

            out = yaml.load(file, Loader=yaml.FullLoader)

        return out

    @staticmethod
    def get_tgroup(columns):

        tgroup = nodes.tgroup(cols=len(columns))

        for column in columns:

            col_width = columns.get(column).get("width")
            col_align = columns.get(column).get("align")

            if col_width is None:

                col_width = 1

            if col_align is None:

                col_align = "left"

            tgroup.append(
                nodes.colspec(
                    colwidth=col_width,
                    colalign=col_align
                )
            )

        return tgroup

    def get_table_body(self, data, columns, target_table=None):

        tbody = nodes.tbody()

        entries = list()

        if isinstance(data, dict):

            for key in data:

                entries.append(data.get(key))

        if isinstance(data, list):

            entries = data

        for entry in entries:

            tbody.append(
                self.get_table_row(
                    data=entry,
                    columns=columns,
                    target_table=target_table
                )
            )

        return tbody

    def get_table_header(self, columns):

        table_header = nodes.thead()

        cols = dict()

        for col in columns.keys():

            cols[col] = columns.get(col).get("name")

        table_header.append(
            self.get_table_row(
                data=cols,
                columns=columns,
                row_format="strong"
            )
        )

        return table_header

    def get_table_row(self, data, columns, row_format=None, target_table=None):

        row = nodes.row()

        row_format = row_format

        if isinstance(data, dict) is False:

            raise ValueError("Argument `data` needs to be a dictionary")

        for col in columns:

            row_entry = nodes.entry()

            cell = data.get(col)

            if cell is None:

                cell = ""

            if row_format is None:

                cell_format = columns.get(col).get("format")

            else:

                cell_format = row_format

            cell_content = self.get_cell_content(
                cell=cell,
                cell_format=cell_format,
                target_table=target_table
            )

            row_entry.append(cell_content)

            row.append(row_entry)

        return row

    @staticmethod
    def get_cell_content(cell, cell_format=None, target_table=None):

        if cell_format is None:

            cell_content = nodes.paragraph(text=str(cell))

        else:

            if cell is None or cell == "":

                cell_content = nodes.paragraph()

            else:

                if cell_format == 'identifier':

                    cell_content = nodes.strong(
                        text=str(cell),
                        ids=["tbl-{table}-col-{column}".format(
                            table=target_table,
                            column=str(cell)
                        )]
                    )

                if cell_format == 'plain-text':

                    if isinstance(cell, (dict, list)):

                        out = yaml.dump(cell, Dumper=CustomDumper, default_flow_style=False)
                        literal = nodes.literal_block(out, out)
                        literal['language'] = 'yaml'
                        cell_content = literal

                    else:

                        out = str(cell)
                        cell_content = nodes.paragraph(text=out)

                if cell_format == 'lookups':

                    if isinstance(cell, dict):

                        cell_content = nodes.paragraph()

                        for key in cell:

                            ref = nodes.reference(cell.get(key), cell.get(key))

                            if key == "table":

                                ref['refuri'] = "#tbl-{table}".format(
                                    table=cell.get(key)
                                )

                            if key == "column":

                                ref['refuri'] = "#tbl-{table}-col-{column}".format(
                                    table=cell.get("table"),
                                    column=cell.get("column")
                                )

                            lit = nodes.literal(text=key+": ")
                            lit.append(ref)

                            cell_content.append(lit)


                if cell_format == 'strong':

                    if isinstance(cell, list):

                        cell_content = nodes.paragraph()

                        for cell_el in cell:

                            cell_content.append(
                                nodes.strong(text=str(cell_el))
                            )
                    else:

                        cell_content = nodes.strong(text=str(cell))

                if cell_format == 'bool':

                    literal = nodes.literal_block(str(cell), str(cell))
                    literal['language'] = 'python'
                    cell_content = literal

                if cell_format == 'literal':

                    if isinstance(cell, list):

                        cell_content = nodes.paragraph()

                        for cell_el in cell:

                            out = cell_el

                            cell_content.append(
                                nodes.literal(text=out)
                            )

                    elif isinstance(cell, dict):

                        out = yaml.dump(cell, Dumper=CustomDumper, default_flow_style=False)

                        literal = nodes.literal_block(out, out)
                        literal['language'] = 'yaml'
                        cell_content = literal

                    else:

                        cell_content = nodes.literal(text=cell)

        return cell_content

    def get_table(self, data, columns, target_table=None):

        table = nodes.table(
            align="left"
        )

        tbl_group = self.get_tgroup(columns=columns)

        tbl_group.append(
            self.get_table_header(
                columns=columns
            )
        )

        tbl_group.append(
            self.get_table_body(
                data=data,
                columns=columns,
                target_table=target_table
            )
        )

        table.append(tbl_group)

        return table

    @staticmethod
    def _transform_dataset_property(data):

        properties = list()

        for el in data.keys():

            if el not in ["columns"]:

                detail = dict()
                detail['table-property'] = el
                detail['property-value'] = data.get(el)
                properties.append(detail)

        return properties

    def run(self):

        current_source = os.path.dirname(
            os.path.abspath(self.state.document.current_source)
        )

        data_source = os.path.join(
            current_source, self.options.get('source')
        )

        data_config = self.load_yaml(path=data_source).get(
            self.options.get('name')
        )

        section = nodes.section(
            ids=["tbl-{table_name}".format(
                table_name=self.options.get('name').lower()
            )],
            level=2
        )

        section_title = "{table_name}".format(
            table_name=self.options.get('name')
        ).capitalize()

        section.append(
            nodes.title(section_title, section_title)
        )

        columns = dict()
        columns["table-property"] = {"name": "Table property", "width": 1, "format": "strong"}
        columns["property-value"] = {"name": "Property value", "width": 5, "format": "plain-text"}

        section.append(
            self.get_table(
                data=self._transform_dataset_property(data_config),
                columns=columns
            )
        )

        section.append(
            nodes.subtitle(text="Columns of table: " + self.options.get('name').capitalize())
        )

        columns = dict()
        columns["name"] = {"name": "Name", "width": 1, "format": "identifier"}
        columns["description"] = {"name": "Description", "width": 5}
        columns["data-types"] = {"name": "Data type", "width": 1, "format": "literal"}
        # columns["max-length"] = {"name": "Max length", "width": 1, "format": "plain-text"}
        # columns["mandatory"] = {"name": "Mandatory", "width": 1, "format": "plain-text"}
        columns["primary-key"] = {"name": "Is primary key", "width": 1, "format": "bool"}
        columns["unique"] = {"name": "Unique", "width": 1, "format": "bool"}
        columns["nullable"] = {"name": "Nullable", "width": 1, "format": "bool"}
        # columns["default"] = {"name": "Default value", "width": 1, "format": "plain-text"}
        # columns["possible-values"] = {"name":"Possible values", "width": 1, "format": "plain-text"}
        columns["source"] = {"name": "source ", "width": 3, "format": "literal"}
        columns["lookups"] = {"name": "Lookup ", "width": 1, "format": "lookups"}

        section.append(
            self.get_table(
                data=data_config.get("columns"),
                columns=columns,
                target_table=self.options.get('name')
            )
        )

        return [section]


def setup(app):
    app.add_directive("data_catalog", DataCatalog)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
