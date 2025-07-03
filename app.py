from controllers.app_controller import AppController

file_path = "data/beauty.xlsx"

if __name__ == "__main__":
    app = AppController(filepath=file_path)
    app.run()
