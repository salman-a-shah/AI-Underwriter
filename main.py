"""
TITLE  : Main executable
AUTHOR : Salman Shah
DATE   : Mon May 27 19:48:36 2019

This file allows a user to type in a file information and make a prediction
"""

def main():
    
    from underwriter import new_user_input
    from underwriter import make_offer
    from underwriter import offer_tostring
    import platform
    import os
    
    CLR = 'cls' if (platform.system().lower()=='windows') else 'clear'
    os.system(CLR)
    
    done = False
    while(not done):
        print("-----------------------")
        print("MCA Machine Underwriter")
        print("-----------------------")
        try:
            user_input = new_user_input()
            print("\n")
            print("Generating offer...")
            offer = make_offer(user_input)
            offer_str = offer_tostring(offer)
        except:
            print("\n------------------------------------------")
            command = input(r"Something went wrong. Press 'Enter' to try again or 'q' to quit: ")
            if (command.lower() == 'q'):
                done = True
            os.system(CLR)
            continue
        
        print("-----------------------------")
        print(offer_str)
        print("-----------------------------")
        cmd = input(r"Press 'Enter' to make evaluate another file or 'q' to quit: ")
        if (cmd.lower() == 'q'):
            done = True

        os.system(CLR)


if __name__ == "__main__":
    main()
