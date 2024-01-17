import sys

def main():
    if len(sys.argv)==1:
        import easy_whisper.tk_ui
    else:
        import easy_whisper.cli_ui
        
if __name__ == "__main__":
    main()

