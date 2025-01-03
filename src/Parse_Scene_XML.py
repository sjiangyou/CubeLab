import os
import xml.etree.ElementTree as ET


def parse(file) -> tuple[list, list[int], str, str, str]:
    node_lst: list = []
    index_lst: list[int] = []
    os.chdir("resources/scenes")
    tree = ET.parse(file)
    root = tree.getroot()
    title, scene_type, background = "", "", ""

    for entry in root.findall("./scene"):
        title, scene_type, background = (
            entry.attrib["title"],
            entry.attrib["type"],
            entry.attrib["background"],
        )
    for entry in root.findall("./list"):
        node = []
        for elem in entry.findall("./textbox"):
            def_str = "Textbox("
            for e in elem.iter():
                def_str += e.text + ", " if e.tag != "textbox" else ""
            def_str = def_str[:-2] + ")"
            node.append(def_str)
        node_lst.append((node, entry.attrib))
        index_lst.append(int(entry.attrib["index"]))
    for entry in root.findall("./textbox"):
        def_str = "Textbox("
        for e in entry.iter():
            def_str += e.text + ", " if e.tag != "textbox" else ""
        def_str = def_str[:-2] + ")"
        node_lst.append((def_str, entry.attrib))
        index_lst.append(int(entry.attrib["index"]))
    for entry in root.findall("./button"):
        def_str = "Button("
        for e in entry.iter():
            def_str += e.text + ", " if e.tag != "button" else ""
        def_str = def_str[:-2] + ")"
        node_lst.append((def_str, entry.attrib))
        index_lst.append(int(entry.attrib["index"]))
    os.chdir("../..")
    return (node_lst, index_lst, title, scene_type, background)


if __name__ == "__main__":
    print(parse("Stackmat_Scene.xml"))
