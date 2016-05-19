# Eyra

TODO: Write a project description

## Installation

### Laptop installation (local wifi)

Run `./Setup/setup.sh --all`

If you want QC to work, you need to install Kaldi, this is done by running `./Setup/setup.sh --ext-kaldi`. This could take some time (hrs).
In addition for the QC, you need to obtain (either by running e.g. `qc/scripts/{Cleanup,Marosijo}GenGraphs.py` or getting it elsewhere) .scp and .ark files containing the decoded graphs. These are used by Marosijo and Cleanup module. Generating them takes a long time, and depends on the number/length of the token list. Look at `qc/scripts/genGraphs.sh` for parallelization of these.

### Internet installation (e.g. for crowdsourcing)

Same as Laptop installation, except begin with `./Setup/setup.sh --all --no-ap`

This should work on both Debian 8 Jessie and Ubuntu Server 14.04. The laptop setup uses a self-signed certificate (which needs to be manually put and installed on the phones), but the internet one should use a real certificate (this depends on which certificate used). We used [letsencrypt](https://letsencrypt.org/) for a free certificate. This has to be done manually.
    
## Usage

Navigate to the website (currently [eyra.ru.is](https://eyra.ru.is)), and you should be good to go.

TODO: Write more detailed usage here.

## Development

### Quick description of folder structure:

* ##### AndroidApp  
    The entire Android app, java code and all. IDE used is Android Studio.

* ##### Backend  
    The Flask python code, which handles connections to the mysql database among other things. Also includes the schema for the database and sql code needed for setup. Recordings are saved in `/data/eyra/recordings/` by default (this can be changed in `app.py` by changing `app.config['MAIN_RECORDINGS_PATH']`, should be an absolute path). Number of useful scripts in `scripts/`.

* ##### Frockend (should be renamed)  
    Code to mock the frontend designed to test the QC (quality control). (not used)

* ##### Frontend  
    The AngularJS code and all related. deploy application using `grunt deploy` in the `da-webapp/` folder. Work in `src/` is then compiled into `app/`.

* ##### Local  
    Locally generated code, generated by the `Setup/setup.sh` script. Used mainly for the apache server.

* ##### Setup  
    Setup of the app. Running `setup.sh` installs the webapp from scratch. Includes code for the apache server, the database setup and the frontend setup.

### Some info
* Look at other README's located within the project (e.g. `Backend/server-interface/qc/README.md` and `Frontend/da-webapp/README.md`) for some more details.

* Logs are located in `Local/Log`. A typical use case would be to for example have a terminal open with a `tail -f {error.log,celery.log}` to watch the apache error log and the celery (QC) log respectively.

* Running `./Setup/setup.sh --all` can be dangerous, because it runs the `--mysqldb` command which deletes the entire database (not the recordings though). Therefore care should be taken when using `--all`, and for example, could run `./Setup/setup.sh --all --no-mysqldb` to leave the database untouched. And of course, remember to backup your database to avoid disasters like this.

### Project maintenance during development

* ##### Routines after checkout from master/origin branch  

    When files are checked out from source some files will change:

    These are: 

    ../Frontend/da-webapp/app/index.html

        --- What to do ----
        index.html files in development and release are different. 
        A backup of the index.html for use in devvelopment environment is at /Frontend/da-webapp/extra_dev_files/dev_index.html. Rename this file as index.html at /Frontend/da-webapp/app/index.html and overwrite the index.html file. A backup copy of the index,html file for use in production is at /Frontend/da-webapp/extra_dev_files/release_index.html.

    ../Frontend/Setup/src/frontend-app/default.conf

        --- What to do ---
        Change 'YYY_SITEROOT=Frontend/da-webapp/app' to YYY_SITEROOT=Frontend/da-webapp/src

        --- What does it do ---
        It changes the path of the index.html file from the one in the 'app' directory root to the on in the 'src' directory root



## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature` (try to follow [this](https://gist.github.com/dmglab/8402579#allowed-prefixes) convention)
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

See a list of our todos in TODOS.md and TODOS_QC.md.

## History

TODO: Write history

## Credits

TODO: Write credits

## License and Notice

This software is Licenced under the Apache Version 2.0 licence as stated in LICENCE document. Some parts of the software are licenced under the MIT licence or other open licences. These differences are noted in NOTICE document. LICENCE and NOTICE documents are found in the root of the data-aquisistion-toolbox project folder.