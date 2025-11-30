import unittest
import os
import time
from computers.playwright.playwright import PlaywrightComputer

class TestRecording(unittest.TestCase):
    def test_recording(self):
        # Simple HTML with a button and an input
        html_content = """
        <html>
        <body>
            <button id="btn1" name="submit_btn" class="primary" style="position:absolute; top:100px; left:100px; width:100px; height:50px;">Click Me</button>
            <input type="text" id="input1" style="position:absolute; top:200px; left:100px; width:200px; height:30px;" />
        </body>
        </html>
        """
        # Save to a temporary file
        with open("test_page.html", "w") as f:
            f.write(html_content)
        
        file_url = "file://" + os.path.abspath("test_page.html")

        # Initialize computer
        # Mock screen size
        screen_size = (1000, 1000)
        
        with PlaywrightComputer(screen_size=screen_size, initial_url=file_url) as computer:
            # Click the button (approx center of 100,100 + 100x50 -> 150, 125)
            computer.click_at(150, 125)
            
            # Type in the input (approx center of 100,200 + 200x30 -> 200, 215)
            computer.type_text_at(200, 215, "hello")

            actions = computer.get_recorded_actions()
            
            print("\nRecorded Actions:")
            for action in actions:
                print(action)

            self.assertEqual(len(actions), 2)
            
            # Verify click action
            click_action = actions[0]
            self.assertEqual(click_action["action"], "click")
            self.assertEqual(click_action["selector"]["id"], "btn1")
            self.assertEqual(click_action["selector"]["tagName"], "BUTTON")
            self.assertEqual(click_action["selector"]["name"], "submit_btn")
            self.assertEqual(click_action["selector"]["className"], "primary")

            # Verify type action
            type_action = actions[1]
            self.assertEqual(type_action["action"], "type")
            self.assertEqual(type_action["selector"]["id"], "input1")
            self.assertEqual(type_action["selector"]["tagName"], "INPUT")
            self.assertEqual(type_action["text"], "hello")

        # Cleanup
        os.remove("test_page.html")

if __name__ == "__main__":
    unittest.main()
