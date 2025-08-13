import alembic.config

def run_alembic_upgrade():
    # Configure Alembic arguments
    alembic_args = [
        '--raiseerr',  # Raise an error if migration fails
        'upgrade',     # Command to upgrade the database
        'head',        # Upgrade to the latest revision
    ]
    
    # Execute the Alembic command
    alembic.config.main(argv=alembic_args)

if __name__ == "__main__":
    run_alembic_upgrade()
    print("Database migration completed successfully.")