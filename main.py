from curueno_porma_warbot.warbot import CuruenoPormaWarbot


if __name__ == "__main__":
    with CuruenoPormaWarbot(
    ) as warbot:
        with warbot.db_manager as db:
            print("Setting up the DB. This is only needed once.")
            db.setup()

        while input("Do you want to exit now? [y/N]").lower() != "y":
            pass
