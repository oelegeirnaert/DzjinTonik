# DzjinTonik

These scripts are used during the migration of DzjinTonik.
So don't use this wrapper in a production environment.

# How to remove a file from GitHub:
https://myopswork.com/how-remove-files-completely-from-git-repository-history-47ed3e0c4c35
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch path_to_file" HEAD
git push
