function form_bootstrap/versions
customfunction remove "form_bootstrap/bootstrap"
customfunction add "form_bootstrap/bootstrap" "result = {func, function.try('form_bootstrap/v1.3')} | err = {func, tuple.get(result, 1)} | if {func, strings.length(err)} > 0: | _ = {command, 'function form_bootstrap/add_forms'} | _ = {command, 'function form_bootstrap/add_funcs'} | _ = {command, 'customfunction add \"form_bootstrap/v1.3\" \"return True\"'} | fi | return True"
customfunction call @s ~ ~ ~ "form_bootstrap/bootstrap"