import time
import argparse
from clapDetector import ClapDetector, printDeviceInfo
import pygame
import webbrowser

def main(use_browser=False):
    print("""
--------------------------------
The application initially attempts to use the system's default audio device. If this doesn't work or if you prefer to use a different device, you can change it. Below are the available audio devices. Find the one you are using and change the 'inputDevice' variable to the name or index of your preferred audio device. Then, restart the program, and it should properly capture audio.
--------------------------------
""")

    printDeviceInfo()

    thresholdBias = 4000
    lowcut = 200
    highcut = 3200

    YOUTUBE_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Substitute with your preferred link
    
    # Handle bundled file path (PyInstaller)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    SOUND_FILE = os.path.join(base_path, "song.mp3")

    clapDetector = ClapDetector(inputDevice=-1, logLevel=10)
    clapDetector.initAudio()

    pygame.mixer.init()

    playing = False

    try:
        while True:
            audioData = clapDetector.getAudio()

            result = clapDetector.run(
                thresholdBias=thresholdBias,
                lowcut=lowcut,
                highcut=highcut,
                audioData=audioData
            )

            if len(result) == 2:
                print(
                    f"Double clap detected! bias {thresholdBias}, "
                    f"lowcut {lowcut}, and highcut {highcut}"
                )

                if use_browser:
                    webbrowser.open(YOUTUBE_LINK)
                else:
                    if not playing:
                        pygame.mixer.music.load(SOUND_FILE)
                        pygame.mixer.music.play()
                        playing = True
                    else:
                        pygame.mixer.music.stop()
                        playing = False

            time.sleep(1 / 60)

    except KeyboardInterrupt:
        print("Exited gracefully")
    except Exception as e:
        print(f"error: {e}")
    finally:
        clapDetector.stop()
        pygame.mixer.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clap detector application")
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Open YouTube link in browser instead of playing sound file"
    )
    args = parser.parse_args()
    main(use_browser=args.browser)