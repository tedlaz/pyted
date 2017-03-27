To delete branch
```
git branch -d <branchname>
git fetch --all --prune
```

To create a signed commit
1. get a list of GPG keys:
```
gpg --list-secret-keys --keyid-format LONG
```
2. Configure git
```
git config --global user.signingkey <key number>
```
3. Commit
```
git commit -S -m your commit message
```
