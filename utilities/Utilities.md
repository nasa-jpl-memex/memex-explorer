Utilities
=========

### Flask Database migrations

Some scripts to help out in database migrations.

For more information: [Flask Database Migrations](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)

##db_create.py

Run once to create database.

After you run the command `python utilities/db_create.py` you will have a new app.db file. This is an empty sqlite database, created from the start to support migrations. You will also have `app/db_repository `with some files inside. This is the place where SQLAlchemy-migrate stores its data files

##db_migrate.py

The way SQLAlchemy-migrate creates a migration is by comparing the structure of the database (obtained in our case from file app.db) against the structure of our models (obtained from file app/models.py). The differences between the two are recorded as a migration script inside the migration repository. The migration script knows how to apply a migration or undo it, so it is always possible to upgrade or downgrade a database format.

##db_upgrade.py

When you run the script, the database will be upgraded to the latest revision, by applying the migration scripts stored in the database repository.


##db_downgrade.py

It is not a common need to have to downgrade a database to an old format, but just in case, SQLAlchemy-migrate supports this as well.

### Tweets preprocessing

##json_to_csv.py

Convert json twitter files into tsv.

