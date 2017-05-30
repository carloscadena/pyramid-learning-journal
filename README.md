# pyramid-learning-journal

#Step 1

Create the following view callables (functions):
list_view: for the list of journal entries
detail_view: for a single journal entry
create_view: for creating a new view
update_view: for updating an existing view

Connect each of the above views to the following routes, with descriptive but concise route names:
/
/journal/{id:\d+}
/journal/new-entry
/journal/{id:\d+}/edit-entry
