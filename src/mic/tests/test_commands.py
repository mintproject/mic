from click.testing import CliRunner


def test_add_parameters():
    test_name = "issue_168"
    result = runner.invoke(inputs, ["-f", mic_config_arg, custom_input_1])
    print(result.output)
    assert result.exit_code == 0
    result = runner.invoke(outputs, ["-f", mic_config_arg])
    print(result.output)
    assert result.exit_code == 0
    result = runner.invoke(wrapper, ["-f", mic_config_arg])
    print(result.output)

    assert result.exit_code == 0
