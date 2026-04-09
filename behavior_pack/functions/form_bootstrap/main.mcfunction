customfunction remove "form_bootstrap/main"
customfunction add "form_bootstrap/main" "_ = {func, function.call('user_interface/panel')} | return True"
customfunction call @s ~ ~ ~ "form_bootstrap/main"
playsound random.toast @s ~ ~ ~ 1.00 1.00 1.00