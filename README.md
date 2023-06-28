## fattr

#### Run

##### Save

```
bin/fattr save -d ~/Software -f ~/Desktop/fattr-2023-06-28.json;
```

##### Restore

```
bin/fattr restore -d ~/Software -f ~/Desktop/fattr-2023-06-28.json;
```

##### Restore (if needed)

```
bin/fattr restore-if-needed -d ~/Software -c ~/Desktop/fattr-2023-06-28.json -p ~/Desktop/fattr-2023-06-27.json;
```

#### License

MIT

#### Author Information

* Mischa ter Smitten (based on work of [mandrawer](https://github.com/robertknight/mandrawer/blob/master/save-file-attrs.py))

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Oefenweb/fattr/issues)!
