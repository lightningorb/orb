#!/bin/bash

alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias gs='git status'
alias ls='ls --color=auto'
alias b='bos balance'
alias pk="lncli getinfo | jq '.identity_pubkey'"
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias get='bos chain-deposit'
alias grep='grep --color=auto'
alias lct="lncli listchaintxns | jq '.transactions[0]'"
alias nct="lncli listchaintxns | jq '.transactions | length'"
alias get="bos chain-deposit"
alias b="bos balance"
alias lnactive='lncli listchannels | jq '\''[ .channels | .[] | select(.active==true) ] | length '\'''
alias send='bos send'
alias towers='lncli wtclient towers'
alias suez='cd ~/src/suez && poetry run ./suez && cd -'
alias failed_events='python3 ~/src/stream-lnd-htlcs/stream-lnd-htlcs.py --stream-mode true | grep link_fail_event'
alias events='python3 ~/src/stream-lnd-htlcs/stream-lnd-htlcs.py --stream-mode true'
alias unlock='/home/ubuntu/.npm-global/bin/bos unlock /home/ubuntu/.lnd/wallet_password'
alias restart_lnd='sudo systemctl restart lnd'
alias deposit='bos chain-deposit'
alias progress="tail -f bitcoind-mainnet.log  | grep -oP 'progress=(\d.\d+)'"