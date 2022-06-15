# grid-pv-sync
Grid connected photovoltaic system of MatER-PUCP syncing file automatization

**Run program in the same directory of the repository**


## Configuration

### client_secrets.json
- Follow instructions from `pydrive2`documentation but use *PC application* not *Web APP*
- Download `client_secrets.json` and paste it to repository folder
### config.json
- Edit folder path of `SFCR_Aplicada`
### crontab
- edit crontab execution `crontab -e`
```shell
0 21 * * * cd <repository_path>; <repository_path>/venv/bin/python <repository_path>/main.py  > crontab.log 2>&1
```