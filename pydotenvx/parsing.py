import re


# TODO: allow to load multiple paths from this
# TODO: validate all paths are ok
def _load_dotenv_file(path: str) -> dict:
    vars = {}
    parse_errors = {}
    with open(path) as f:
        for i, line in enumerate(f.readlines(), start=1):
            line = line.strip()
            if not line:
                continue
            if "=" not in line:
                parse_errors[i] = f"Missing assignment: {line}"
            if '"' not in line:
                parse_errors[i] = f"Missing quotes: {line}"

            # TODO: assure only one var per line
            pattern = r'^\s*([^"\s]+)\s*=\s*"([^"]+)"\s*$'
            matches = re.findall(pattern, line)

            if len(matches) == 0:
                parse_errors[i] = f"Could not parse: {line}"
                continue

            for match in matches:
                key, value = match

            vars[key] = value

    if len(parse_errors) > 0:
        msg = "Could not parse the following lines:\n"
        parse_errors = [f"{path}:{i} - {err}" for i, err in parse_errors.items()]
        msg += "\n".join(parse_errors)
        raise ValueError(msg)

    return vars
