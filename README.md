tools
=====
ops tools
bashrc记录操作
export PROMPT_COMMAND='{ msg=$(history 1 | { read x y; echo $y; });logger "[hostname- $(hostname)]": "[euid=$(whoami)]":$(who am i):[`pwd`]:"$msg"; }'
export PS1='[\[$(tput bold)$(tput setb 4)$(tput setaf 1)\]\u@\h ~ \A \[$(tput bold)$(tput setb 4)$(tput setaf 2)\]\w\[$(tput bold)$(tput setb 4)$(tput setaf 7)\]]\[$(tput bold)$(tput setb 4)$(tput setaf 6)\]\#\$\[$(tput bold)$(tput setb 4)$(tput setaf 7)\]'
