from aegis.ast import Block, Mission, NumberLiteral, SourceLocation, PowerCommand, ast_to_dict


def test_ast_nodes_preserve_structure_and_location() -> None:
    value = NumberLiteral(80, location=SourceLocation(2, 11))
    command = PowerCommand(value, location=SourceLocation(2, 5))
    mission = Mission(
        "observation",
        Block((command,), location=SourceLocation(1, 21)),
        location=SourceLocation(1, 1),
    )

    assert mission.name == "observation"
    assert mission.body.statements[0].value.value == 80
    assert mission.body.statements[0].location == SourceLocation(2, 5)
    assert ast_to_dict(mission)["type"] == "Mission"
