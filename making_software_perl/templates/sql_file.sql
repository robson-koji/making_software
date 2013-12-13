    [% FOREACH choice_id = sql.choices.keys %]
        INSERT INTO [% sql.slug %]_choices_[% sql.field_slug %] (choice_desc) VALUES ('[% sql.choices.$choice_id.label %]');
    [% END %]  

