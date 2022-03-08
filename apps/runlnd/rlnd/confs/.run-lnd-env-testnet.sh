# this is the env file used to set up your paths / aliases properly for
# lnd, and bos

# set up GOPATH for general go usage
GOPATH="$HOME/go"

# set up the PATH, so we can invoke bos directly
PATH="$HOME/.npm-global/bin:$PATH"

# set up the path, so we can invoke lnd and go directly
PATH="$HOME/bin:$GOPATH/bin:$HOME/.local/bin:/usr/local/go/bin:$PATH"

if command -v bos &> /dev/null
then
    source <(bos completion bash)
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

cat << EOF

           ,/
         ,'/
       ,' /
     ,'  /_____,
   .'____    ,'
        /  ,'
       / ,'
      /,'
     /'

EOF

echo "alias: $(lncli getinfo | jq '.alias')"
echo "lnd: $(lncli version | jq '.lnd.commit')"
bitcoin-cli -version
echo "bos: $(bos --version)"

# use the --testnet flag for lncli
alias lncli="lncli --network=testnet ${*}"
