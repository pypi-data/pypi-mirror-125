from subprocess import CalledProcessError, check_output

from recoverpy.utils.logger import LOGGER


class MenuWithBlockDisplay:
    """Composition aimed class for menus needing methods to display partition
    blocks content.

    Attributes:
        master (PyCUI): PyCUI main object for UI.
        horizontal_char_limit (int): Number of chars that can fit horizontally in
            the left hand result box.
        current_block (int): Partition block number currently displayed.
        current_result (int): Block text content found with dd command.
        result_content_box (PyCUI.TextBox): TextBox in which dd command result
            will be displayed.
        partition (str): System partition selected by user for search.
    """

    def __init__(self):
        """Initialize MenuWithBlockDisplay."""
        self.master = None

        self.horizontal_char_limit = 0

        self.current_block = None
        self.current_result = None

        self.result_content_box = None
        self.partition = None

    def get_dd_result(self, block: str = None):
        """Store a 'dd' command result in current_result var.

        Args:
            block (str): Partition block number. Defaults to None.
        """
        if block is None:
            block = self.current_block

        LOGGER.write(
            "debug",
            f"Getting 'dd' output for block {str(self.current_block)}",
        )

        try:
            dd_result = check_output(
                [
                    "dd",
                    f"if={self.partition}",
                    "count=1",
                    "status=none",
                    f"skip={block}",
                ]
            )
            # Try/Catch to decode raw result in utf-8
            try:
                self.current_result = dd_result.decode("utf-8")
            except UnicodeDecodeError:
                self.current_result = str(dd_result)
            self.current_block = block

            LOGGER.write("debug", "dd command successful")
        except CalledProcessError:
            self.master.show_error_popup(
                "Mmmmhhh...",
                f"Error while opening block {str(self.current_block)}",
            )
            LOGGER.write(
                "error",
                f"Error while opening block {str(self.current_block)}",
            )

    def update_textbox(self):
        """Format 'dd' result by breaking lines by char_limit and display it."""
        self.update_char_limit()

        # Format raw result to display it in the text box
        result_lines = [
            str(self.current_result)[i : i + self.horizontal_char_limit]
            for i in range(0, len(str(self.current_result)), self.horizontal_char_limit)
        ]
        formated_result = "\n".join(result_lines)

        # TEMPORARY FIX for embedded null character
        formated_result = formated_result.replace(chr(0), "")

        self.result_content_box.set_text(formated_result)
        self.result_content_box.set_title(f"Block {self.current_block}")

        LOGGER.write("debug", f"Textbox updated with block {self.current_block}")

    def display_previous_block(self):
        """Display block n-1 in textbox."""
        try:
            self.display_block(str(int(self.current_block) - 1))
        except ValueError:
            LOGGER.write("error", f"Cannot display block {self.current_block} - 1")
            return

    def display_next_block(self):
        """Display block n+1 in textbox."""
        try:
            self.display_block(str(int(self.current_block) + 1))
        except ValueError:
            LOGGER.write("error", f"Cannot display block {self.current_block} + 1")
            return

    def display_block(self, block: str):
        """Display given block number in textbox.

        Args:
            block (str): Partition block number.
        """
        if int(block) < 0:
            return

        self.get_dd_result(block=block)
        self.update_textbox()

    def update_char_limit(self):
        """Update horizontal character limit for textbox depending on terminal size."""
        text_box_dimensions = self.result_content_box.get_cursor_limits_horizontal()
        self.horizontal_char_limit = text_box_dimensions[1] - text_box_dimensions[0]
        LOGGER.write(
            "debug",
            f"Textbox char limit set to {self.horizontal_char_limit}",
        )
