from pathlib import Path


def generate_large_valid_fixture(path: Path, count: int = 120):
    requirements = []
    for index in range(1, count + 1):
        requirements.append(
            f'''      <req id="REQ-PERF-{index:03d}" type="FR" title="Performance requirement {index}" status="approved" priority="must">\n'''
            f'''        <statement>The fixture SHALL support performance validation row {index}.</statement>\n'''
            f'''        <acceptance>\n'''
            f'''          <criterion id="CRIT-PERF-{index:03d}">\n'''
            f'''            <then>The row {index} is structurally valid.</then>\n'''
            f'''          </criterion>\n'''
            f'''        </acceptance>\n'''
            f'''      </req>'''
        )

    content = f'''<?xml version="1.0" encoding="UTF-8"?>\n<rqml xmlns="https://rqml.org/schema/2.1.0" version="2.1.0" docId="FIXTURE-PERF" status="draft">\n  <meta>\n    <title>Performance Fixture</title>\n    <system>fixture-skill</system>\n  </meta>\n  <requirements>\n    <reqPackage id="PKG-PERF" title="Performance package">\n''' + "\n".join(requirements) + '''\n    </reqPackage>\n  </requirements>\n</rqml>\n'''
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    generate_large_valid_fixture(Path("tests/fixtures/perf-valid-2.1.0.rqml"))
