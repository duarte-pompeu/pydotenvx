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

            key = ""
            value = ""
            mode = ""

            parsing_line = (c for c in line)

            for char in parsing_line:
                if not mode:
                    if char.isspace():
                        continue
                    if char == "#":
                        mode = "ONLY COMMENT"
                        break
                    if char == "=":
                        parse_errors[i] = f"Missing key: {line}"
                    else:
                        mode = "PROCESSING_KEY"
                        key += char
                elif mode == "PROCESSING_KEY":
                    if char.isspace():
                        mode = "END_OF_KEY"
                        continue
                    if char == "=":
                        break
                    else:
                        key += char
                elif mode == "END_OF_KEY":
                    if char == "=":
                        break
                    if not char.isspace():
                        parse_errors[i] = f"Invalid key: {line}"
                else:
                    raise ValueError(f"Unknown mode: {mode}")

            if mode == "ONLY COMMENT":
                continue

            mode = ""
            for char in parsing_line:
                if not mode:
                    if char.isspace():
                        continue
                    if char == '"':
                        mode = "PROCESSING_VALUE"
                        continue
                    else:
                        parse_errors[i] = (
                            f"Expected quote after assignment but got something else: {line}"
                        )
                elif mode == "PROCESSING_VALUE":
                    if char == "\\":
                        mode = "ESCAPED_VALUE"
                        continue
                    if char == '"':
                        mode = "END_OF_VALUE"
                        continue
                    else:
                        value += char
                elif mode == "ESCAPED_VALUE":
                    mode = "PROCESSING_VALUE"
                    value += char
                    continue
                elif mode == "END_OF_VALUE":
                    if char.isspace():
                        continue
                    if char == "#":
                        break
                else:
                    raise ValueError(f"Unknown mode: {mode}")

            vars[key] = value

    if len(parse_errors) > 0:
        msg = "Could not parse the following lines:\n"
        parse_errors = [f"{path}:{i} - {err}" for i, err in parse_errors.items()]
        msg += "\n".join(parse_errors)
        raise ValueError(msg)

    return vars
