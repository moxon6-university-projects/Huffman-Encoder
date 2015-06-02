from tkFileDialog import askopenfilename, asksaveasfilename
from Tkinter import Tk, Label, Button, X
import huffenc
import sys
import hashlib


class DialogBox:
    """
    Dialog Box Class

    Simply displays the message in `report`

    Attributes:
        root (Tk) : Tk root widget
    """

    def __init__(self, report):
        """
        Creates Dialog box and displays it

        Args:
            report (str) : String to display in Dialog box
        """
        self.root = Tk()
        Label(self.root, text=report).pack(fill=X)
        Button(self.root, text='Quit', command=self.quit).pack(fill=X)
        self.root.mainloop()

    def quit(self):
        """
        Destroys Dialog box
        """
        self.root.destroy()
        self.root.quit()


class EncodingDialog:

    def __init__(self):

        self.root = Tk()
        self.root.wm_title("Martin's Awesome Huffman Encoder")
        self.root.wm_minsize(width=375, height=0)

        Button(self.root, text='Encode', command=self.encode).pack(fill=X)
        Button(self.root, text='Decode', command=self.decode).pack(fill=X)
        Button(self.root, text='SHA-1 Compare', command=self.sha).pack(fill=X)
        self.enc = "DEFAULT"
        self.root.mainloop()

    def encode(self):
        self.enc = "encode_file"
        self.root.destroy()

    def decode(self):
        self.enc = "decode_file"
        self.root.destroy()

    def sha(self):
        self.enc = "sha"
        self.root.destroy()


def huffman_main(encoding_mode, input_path, output_path):
    try:
        if encoding_mode not in ['encode_file', 'decode_file']:
            print "Encoding type must either be \'encode_file\' or \'decode_file\'"
            raise Exception
        if len(output_path) == 0:
            output_path = huffenc.get_default_path(input_path, encoding_mode == "encode_file")
    except Exception as e:
        print str(e)
        print 'Usage: \"python Huffman_GUI.pyw enc input output\" \nenc is either \'encode_file\' or \'decode_file\' for ' +\
              'encoding or decoding. \ninput is the input path. \noutput is the output path.'

    if encoding_mode == "encode_file":
        huffenc.encode_file(input_path, output_path)
    elif encoding_mode == "decode_file":
        huffenc.decode_file(input_path, output_path)


def get_file_paths(enc_type):
    file_type_list = [
        ("ASCII/UTF-8 Encoded Plaintext", ".txt"),
        ("All files", "*.*"),
        ("Martin's Awesome Huffman Format", ".hc")
        ]
    open_path = close_path = ""
    root = Tk()
    root.withdraw()
    if enc_type == "encode_file":
        open_path = askopenfilename(parent=root, defaultextension=".txt", filetypes=file_type_list)
        close_path = asksaveasfilename(defaultextension=".hc", filetypes=[file_type_list[2]])
    elif enc_type == "decode_file":
        open_path = askopenfilename(parent=root, defaultextension=".hc", filetypes=[file_type_list[2]])
        close_path = asksaveasfilename(defaultextension=".txt", filetypes=file_type_list)
    if open_path == "" or close_path == "":
        raise Exception
    return open_path, close_path


def gui_huffman():
    try:
        enc_box = EncodingDialog()
        enc_type = enc_box.enc

        if enc_type in ["encode_file", "decode_file"]:
            open_path, close_path = get_file_paths(enc_type)
            huffman_main(enc_type, open_path, close_path)
        elif enc_type == "sha":
            compare()

        DialogBox('Process Completed Successfully.')

    except Exception as e:
        print str(e)


def command_line_huffman():
    huffman_main(sys.argv[1], sys.argv[2], sys.argv[3])


def compare():
    try:
        box = Tk()
        box.withdraw()
        file1 = askopenfilename(filetypes=[("All files", "*.*")])
        file2 = askopenfilename(filetypes=[("All files", "*.*")])
        box.destroy()
    except Exception as e:
        return str(e)
    try:
        file1 == file2  # Checks for existence of both file1 and file2
    except Exception as e:
        print str(e)
        return None

    file_1 = open(file1, 'rb')
    hash1 = hashlib.sha1(file_1.read()).hexdigest()
    file_1.close()

    file_2 = open(file2, 'rb')
    hash2 = hashlib.sha1(file_2.read()).hexdigest()
    file_2.close()

    if hash1 == hash2:
        report = "SHA-1 hashes are equivalent. No errors were made in the encoding-decoding process for this file."
    else:
        report = "SHA-1 hash inconsistency. Errors were made in the encoding-decoding process for this file."
    DialogBox(report)


def main():
    """
    If no parameters are given, use GUI method,
    otherwise act in command line mode
    """
    if len(sys.argv) == 1:
        gui_huffman()
    else:
        command_line_huffman()

if __name__ == "__main__":
    main()
