from jsondatahelper import KEY_SPLIT_CHAR, flatten, subpath_value
import json

DEFAULT_PLURAL_ID = "s"
OBJECT_NAME = "name"
OBJECT_ATTRIBUTE = "attribute"
ATTRIBUTES = "attributes"
FUNCTIONS = "functions"
VARIABLE_NAMES = "variable Names"
VARIABLE_VALUES = "variable Values"

JSONLINK_ATTRIBUTE_FILTERS = [
    "append_subclass_object",
    "update_from_dict",
    "is_function",
    "create_example",
    "get_state",
]

GET_STATE_FILTERS = [
    "keywords",
    "sub_classes",
    "attribute_keyword_links",
    "sub_class_containers",
    "functions",
    "attributes",
    "properties",
    "variables",
    "name",
    "plural_identifier",
    "variable_values",
    "default_state",
]

PRIMATIVE_DEFAULTS = {"str": "", "list": [], "dict": {}, "int": 0}


def filter_dict(dictionary, filter_list=[]):
    return {k: v for k, v in dictionary.items() if k not in filter_list}


def get_default_primative(variable_value):
    try:

        return PRIMATIVE_DEFAULTS[type(variable_value).__name__]
    except KeyError:
        return ""


def primative_default_list(list_of_values):

    return [get_default_primative(value) for value in list_of_values]


def write_to_file(file_path, data):
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=True,
            indent=4,
        )


def pythonic(obj):
    if isinstance(obj, list):
        return pythonic_list(obj)
    elif isinstance(obj, str):
        return pythonic_string(obj)
    else:
        print(
            "Object type not supported", str(type(obj)), "for python string conversion"
        )


def pythonic_list(lst):
    return [pythonic_string(string) for string in lst]


def pythonic_string(string):
    return string.replace(" ", "_").lower()


def english(string):
    s = ""
    for word in string.split("_"):
        s = s + word.capitalize() + " "
    return s.rstrip()


def lists_are_equal(list_one, list_two):
    return len(list_intersection(list_one, list_two)) == len(list_one)


def list_intersection(list_one, list_two):
    if list_one and list_two:
        return list(set(list_one) & set(list_two))


def pythonic_list_intersection(list_one, list_two):
    return list_intersection(pythonic(list_one), pythonic(list_two))


def convert_bytes(loaded_json):
    for key, val in loaded_json.items():
        if isinstance(val, dict):
            loaded_json[key] = convert_bytes(val)
        elif isinstance(val, list):
            for index, item in enumerate(val):
                if isinstance(item, dict):
                    loaded_json[key][index] = convert_bytes(item)
                elif isinstance(item, str) and item.startswith("b'"):
                    loaded_json[key][index] = bytes.fromhex(item.split("b'")[1])
        elif isinstance(val, str) and val.startswith("b'"):
            loaded_json[key] = bytes.fromhex(val.split("b'")[1])

    return loaded_json


def read_json_file(file_path):
    try:
        with open(file_path, "r+") as file_contents:
            return convert_bytes(json.load(file_contents))
    except FileNotFoundError:
        return None


def get_attributes(object_reference, filters=["__"]):
    functions = dir(object_reference)
    filtered_functions = dir(object_reference)
    for function_name in functions:
        for filter in filters:
            if filter in function_name:
                try:
                    filtered_functions.remove(function_name)
                except ValueError:
                    pass  # Value Already removed

    return filtered_functions


def get_variables(object):
    return list(object.__dict__.keys()), list(object.__dict__.values())


def is_instanciated(object):
    return "." in str(type(object))


def splunk(object, attribute_filters=["__"], *args, **kwargs):
    """
    Gathers all object attributes (function names & variables) and returns them as a dictionary:
    Attribute filter will filter out any attributes that input string is found in.
    """
    if not is_instanciated(object):  # If not instanciated
        object = object()

    object_name = type(object).__name__
    object_attributes = get_attributes(object, attribute_filters)
    object_variable_names, object_variable_values = get_variables(object)
    object_functions = list(
        set(object_attributes).difference(set(object_variable_names))
    )
    object_functions.sort()

    return {
        OBJECT_NAME: object_name,
        ATTRIBUTES: object_attributes,
        FUNCTIONS: object_functions,
        VARIABLE_NAMES: object_variable_names,
        VARIABLE_VALUES: object_variable_values,
    }


def get_indexes(path, return_last_found=False):
    """
    'path' represents a single property in flattend dictionary
    input  : this->is->1->a->path
    intermediate : ["this","is",1,"a","path"]
    output : [1]
    """
    # v: String representation of index in path

    found_indexes = [v for v in path.split(KEY_SPLIT_CHAR) if v.isdigit()]
    if found_indexes:
        if return_last_found:
            return found_indexes[-1]
    else:
        return -1
    return found_indexes


class SubClass:
    def __init__(self, class_reference):
        self.properties = splunk(class_reference, attribute_filters=["__"])
        self.class_reference = class_reference
        self.name = self.properties[OBJECT_NAME].lower()
        self.attributes = self.properties[ATTRIBUTES]
        self.variables = self.properties[VARIABLE_NAMES]
        self.variable_values = self.properties[VARIABLE_VALUES]
        self.functions = self.properties[FUNCTIONS]

    def build_new(self):
        return self.class_reference()

    def has_attribute(self, attribute):
        return attribute in self.attributes

    def is_function(self, function_name):
        return function_name in self.functions


class KeywordAttributeLink:
    def __init__(self, attribute, class_name="", is_function=False):
        self.attribute = attribute
        self.class_name = class_name
        self.is_function = is_function

    # def __repr__(self):
    #     return f"""
    #     [ATTRIBUTE LINK]
    #         Name        : {self.attribute}
    #         Class       : {self.class_name}
    #         Is Function : {self.is_function}
    #     """


class JsonLink:
    def __init__(
        self,
        sub_classes=[],
        attribute_filters=["__"],
        keywords_file_path="",
        use_keywords_file=False,
        plural_identifier=DEFAULT_PLURAL_ID,
    ):
        self.__add_jsonlink_attribute_filters(attribute_filters)
        self.properties = splunk(self, attribute_filters=attribute_filters)
        self.plural_identifier = plural_identifier
        self.__set_meta_variables()
        self.__build_keywords()
        self.__associate_sub_classes(sub_classes)
        self.__read_keywords_file(keywords_file_path, use_keywords_file)
        self.__associate_keywords_to_attributes()

    def __add_jsonlink_attribute_filters(self, attribute_filters):
        for attribute in JSONLINK_ATTRIBUTE_FILTERS:
            attribute_filters.append(attribute)
        return attribute_filters

    def __set_meta_variables(self):
        self.name = self.properties[OBJECT_NAME]
        self.attributes = self.properties[ATTRIBUTES]
        self.functions = self.properties[FUNCTIONS]
        self.variables = self.properties[VARIABLE_NAMES]
        self.variable_values = self.properties[VARIABLE_VALUES]
        self.default_state = dict(
            zip(self.variables, primative_default_list(self.variable_values))
        )

    def __build_keywords(self):
        self.keywords = {}
        for attribute in self.properties[ATTRIBUTES]:
            self.keywords[pythonic(attribute)] = []

    def __associate_sub_classes(self, sub_classes):

        self.sub_classes = {}
        if sub_classes:
            for class_reference in sub_classes:
                sub_class = SubClass(class_reference)
                self.sub_classes[sub_class.name] = sub_class
                sub_class_container_name = sub_class.name + self.plural_identifier
                self.default_state[sub_class_container_name] = [
                    dict(
                        zip(
                            sub_class.properties[VARIABLE_NAMES],
                            primative_default_list(
                                sub_class.properties[VARIABLE_VALUES],
                            ),
                        )
                    )
                ]
                setattr(self, sub_class_container_name, [])
                for sub_class_attribute in sub_class.attributes:
                    self.keywords[pythonic(sub_class_attribute)] = []

    def __purge_sub_class_containters(self):
        for sub_class_name in self.sub_classes:
            setattr(self, sub_class_name + self.plural_identifier, [])

    def __read_keywords_file(self, keywords_file_path, use_keywords_file):
        if use_keywords_file or keywords_file_path:
            if (
                not keywords_file_path
            ):  # Set Default Keywords file for given class object
                keywords_file_path = (
                    self.properties[OBJECT_NAME] + "_keywords" + ".json"
                )

            found_keywords_file_contents = read_json_file(keywords_file_path)

            if not found_keywords_file_contents:  # If file not found, create new
                write_to_file(keywords_file_path, self.keywords)

            elif not lists_are_equal(
                self.keywords.keys(), found_keywords_file_contents.keys()
            ):
                for key in self.keywords.keys():
                    try:
                        found_keywords_file_contents[key]
                    except KeyError:
                        found_keywords_file_contents[key] = []

                write_to_file(keywords_file_path, found_keywords_file_contents)
                self.keywords = found_keywords_file_contents
            else:
                self.keywords = found_keywords_file_contents
        else:
            pass  # Keyword are already set in __build_keywords and __associate_sub_classes

    def __associate_keywords_to_attributes(self):
        """
        Associates Keyword File in local directory to functions
        in this class.
        """

        self.attribute_keyword_links = {}
        for default_keyword, keyword_aliases in self.keywords.items():
            default_keyword = pythonic(default_keyword)
            attribute_link = None
            if default_keyword in self.attributes:
                attribute_link = KeywordAttributeLink(
                    default_keyword, self.name, self.is_function(default_keyword)
                )
            else:
                attribute_link = self.__find_sub_class_attribute(default_keyword)

            if attribute_link:
                self.attribute_keyword_links[default_keyword] = attribute_link
                for alias in keyword_aliases:
                    self.attribute_keyword_links[pythonic(alias)] = attribute_link

    def __find_sub_class_attribute(self, keyword):
        for sub_class in self.sub_classes.values():
            if sub_class.has_attribute(keyword):
                class_name = sub_class.name
                return KeywordAttributeLink(
                    keyword,
                    class_name,
                    self.sub_classes[class_name].is_function(keyword),
                )

    def __process_attribute(
        self, property_name, property_value, sub_class_container_index=-1
    ):
        property_name = pythonic(property_name)
        try:

            attribute_link = self.attribute_keyword_links[property_name]

            perform_action_on_this = None
            if attribute_link.class_name == self.name:
                perform_action_on_this = self

            elif int(sub_class_container_index) >= 0:  # Is sub class object
                sub_class_object = self.__get_subclass_item(
                    attribute_link.class_name, sub_class_container_index
                )

                if not sub_class_object:
                    sub_class_name = attribute_link.class_name
                    new_object = self.__new_subclass_object(sub_class_name)
                    sub_class_object = self.__append_subclass_object(
                        sub_class_name, new_object
                    )

                perform_action_on_this = sub_class_object

            if perform_action_on_this:
                self.__perform_attribute_action(
                    instanciated_object=perform_action_on_this,
                    attribute_link=attribute_link,
                    property_value=property_value,
                )

        except KeyError:
            print(f"{property_name} not found!")
            return False  # Attribute not found
        return True  # Attribute found

    def __get_subclass_container(self, class_name):
        return getattr(self, class_name.lower() + self.plural_identifier)

    def __append_subclass_object(self, class_name, obj):
        self.__get_subclass_container(class_name).append(obj)
        return self.__get_subclass_container(class_name)[-1]

    def __get_subclass_item(self, sub_class_name, sub_class_container_index):
        try:
            return self.__get_subclass_container(sub_class_name)[
                int(sub_class_container_index)
            ]
        except IndexError:  # Item Does Not Exist
            return None

    def __new_subclass_object(self, class_name):
        return self.sub_classes[class_name].build_new()

    def run_function(self, instanciated_object, function_name, property_value={}):
        return getattr(instanciated_object, function_name)(property_value)

    def __perform_attribute_action(
        self, instanciated_object, attribute_link, property_value
    ):

        if attribute_link.is_function:
            getattr(instanciated_object, attribute_link.attribute)(property_value)
        else:
            found_attribute = getattr(instanciated_object, attribute_link.attribute)
            if isinstance(found_attribute, dict):
                property_value.update(found_attribute)
            if isinstance(property_value, list):
                pass

            setattr(instanciated_object, attribute_link.attribute, property_value)

    def is_function(self, function_name):
        return function_name in self.properties[FUNCTIONS]

    def append_subclass_object(self, sub_class_name, attributes={}):
        pythonic_class_name = pythonic(sub_class_name)
        sub_class_object = self.sub_classes[pythonic_class_name].build_new()

        for attribute_name, attribute_value in attributes.items():
            setattr(sub_class_object, attribute_name, attribute_value)

        self.__append_subclass_object(sub_class_name, sub_class_object)

    def update_from_dict(self, dictionary):
        self.__purge_sub_class_containters()

        for property_path, property_value in flatten(dictionary).items():

            split_path = property_path.split(KEY_SPLIT_CHAR)
            found_keywords = pythonic_list_intersection(
                list(self.attribute_keyword_links.keys()), split_path
            )
            if found_keywords:
                found_keyword = found_keywords[0]
                if not found_keyword == split_path[len(split_path) - 1]:
                    property_value = subpath_value(
                        {pythonic(property_path): property_value}, found_keyword
                    )

                self.__process_attribute(
                    found_keyword,
                    property_value,
                    get_indexes(property_path, return_last_found=True),
                )

        return self

    def get_state(self):

        state = filter_dict(self.__dict__, GET_STATE_FILTERS)

        for sub_class in self.sub_classes.keys():

            container_name = sub_class + self.plural_identifier
            container = getattr(self, container_name)
            state[container_name] = []
            for item in container:
                state[container_name].append(item.__dict__)
        return state

    def save_default_state(self, file_path=""):
        file_name = "default_" + self.name + ".json"
        if not file_path:
            file_path = file_name
        write_to_file(file_path, self.default_state)

    def __repr__(self):
        return f"""
            Object Name : {self.name}\n
            Attributes  : {self.attributes}\n
            Variables   : {self.variables}\n
            Functions   : {self.functions}\n
            Keywords    : {self.keywords}\n
            Sub Classes : {self.sub_classes}\n                       
        """
