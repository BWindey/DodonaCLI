# Bash completion script for DodonaCLI, needs to be sourced to work
# Used https://www.gnu.org/software/gnuastro/manual/html_node/Bash-TAB-completion-tutorial.html to help create this

# $1 = name of command -> dodona
# $2 = current word being completed
# $3 = word before word being completed

_dodona(){
    if [ "$3" == "sub" ]; then
        COMPREPLY=( $(compgen -W "load display --help" -- "$2")  )

    elif [ "$3" == "display" ]; then
        COMPREPLY=( $(compgen -W "--force --help" -- "$2") )

    elif [ "$3" == "info" ]; then
        COMPREPLY=( $(compgen -W "version changelog github check-update"))

    elif [ "$3" == "select" ]; then
        COMPREPLY=( $(compgen -W "--other --hidden --help" -- "$2") )

    elif [ "$3" == "next" ]; then
        COMPREPLY=( $(compgen -W "--reverse --unsolved --help" -- "$2") )

    elif [ "$3" == "dodona" ]; then
        COMPREPLY=( $(compgen -W "display info next post select status sub tutorial up --help" -- "$2") )

    elif [ "$3" == "post" ]; then
        COMPREPLY=( $(compgen -f -- "$2" | grep -vF ".swp") $(compgen -W "--help --use-link -l -c --check" -- "$2" ))

    elif [[ "$3" =~ ^-[lc]+$ ]] || [ "$3" == "--use-link" ] || [ "$3" == "--check" ]; then
        COMPREPLY=( $(compgen -f -- "$2") )

    elif [ "$3" == "up" ]; then
        COMPREPLY=( $(compgen -W "all top 1 2 3" -- "$2") )

    else
        COMPREPLY=( $(compgen -W "--help") )
    fi
}

complete -F _dodona dodona
