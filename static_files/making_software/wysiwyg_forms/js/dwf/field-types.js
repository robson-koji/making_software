define(function (require, exports, module) {

    exports.FIELD_TYPES = [
        { fieldType: "CharField",
          widget: "TextInput",
          description: "Texto curto" },

        { fieldType: "CharField",
          widget: "Textarea",
          description: "Texto longo" },

        { fieldType: "BooleanField",
          widget: "CheckboxInput",
          description: "Checkbox - Falso ou verdadeiro" },

        { fieldType: "ChoiceField",
          widget: "Select",
          description: "Select - Opção simples",
          hasChoices: true },
          
        { fieldType: "MultipleChoiceField",
          widget: "CheckboxSelectMultiple",
          description: "Select - Múltiplas opções",
          hasChoices: true },
          
        { fieldType: "IntegerField",
          widget: "TextInput",
          description: "Número (sem ponto decimal)" },
          
        { fieldType: "FloatField",
          widget: "TextInput",
          description: "Número (com ou sem ponto decimal)" },

        { fieldType: "CharField",
          widget: "TextInput",
          description: "Dinheiro",
          mask: "money" },          
          
        { fieldType: "DateField",
          widget: "DateInput",
          description: "Data" },
        
        { fieldType: "TimeField",
          widget: "TextInput",
          description: "Hora" },
          
        { fieldType: "DateTimeField",
          widget: "DateTimeInput",
          description: "Data e hora" },

        { fieldType: "EmailField",
          widget: "TextInput",
          description: "Email" },

        { fieldType: "IPAddressField",
          widget: "TextInput",
          description: "Endereço IP" },

        { fieldType: "URLField",
          widget: "TextInput",
          description: "URL hyperlink" },

        { fieldType: "FileField",
          widget: "FileInput",
          description: "Upload de arquivo" },

        { fieldType: "ImageField",
          widget: "FileInput",
          description: "Upload de imagem" },


    ];

    // Iterate over each of the field types, return false to break out of the
    // iteration.
    exports.eachFieldType = function (fn, ctx) {
        var ret = true;
        var i = 0;
        var len = exports.FIELD_TYPES.length
        ctx = ctx || {};
        for ( ; i < len && ret !== false; i++ ) {
            ret = fn.call(ctx, exports.FIELD_TYPES[i]);
        }
    };

    // Returns true if the given field type has choices.
    exports.hasChoices = function (type) {
        var ret = false;
        exports.eachFieldType(function (t) {
            if ( t.fieldType === type && t.hasChoices ) {
                ret = true;
                return false;
            }
        });
        return ret;
    };

});
