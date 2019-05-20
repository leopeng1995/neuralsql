from bson.code import Code


# TODO this way only used in english.
def generate_mapper(column):
    tpl_prev = """
        function() {
            var words_list = this."""

    tpl_next = """.split(' ');
    
            var words_dict = {};
            for (var i = 0; i < words_list.length; i++) {
                var key = words_list[i].toLowerCase();
                if (words_dict.hasOwnProperty(key)) {
                    words_dict[key] = words_dict[key] + 1;
                } else {
                    words_dict[key] = 1;
                }
            }
    
            for (var key in words_dict) {
                emit(key, words_dict[key]);
            }
        }
    """
    code_string = tpl_prev + column + tpl_next
    return Code(code_string)


def generate_reducer():
    tpl = """
        function (key, values) {
            return Array.sum(values);
        }
    """
    return Code(tpl)
