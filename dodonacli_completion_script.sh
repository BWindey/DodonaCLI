# Bash completion script for the Dodona command, needs to be sourced to work
# Used https://www.gnu.org/software/gnuastro/manual/html_node/Bash-TAB-completion-tutorial.html

# $1 = name of command -> dodona
# $2 = current word being completed
# $3 = word before word being completed

_dodona(){
	if [ "$3" == "sub" ]; then
		COMPREPLY=( $(compgen -W "load display" -- "$2")  )

	elif [ "$3" == "display" ]; then
		COMPREPLY=( $(compgen -W "-force" -- "$2") )

	elif [ "$3" == "dodona" ]; then
		COMPREPLY=( $(compgen -W "display post select status sub tutorial up" -- "$2") )
	
	elif [ "$3" == "post" ]; then
		COMPREPLY=( $(ls -Ap | grep -v "/" | grep "$2") )
	fi
}

complete -F _dodona dodona
