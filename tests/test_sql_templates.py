import jinja2
import pathlib

SQL_DIR = pathlib.Path(__file__).parents[1] / "sql"

def test_all_sql_templates_render():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(SQL_DIR)))
    for sql_file in SQL_DIR.glob("*.sql"):
        template = env.get_template(sql_file.name)
        rendered = template.render()  # pas de variables → doit passer
        assert "SELECT" in rendered.upper()
