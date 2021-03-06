#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import copy

from openstackclient.identity.v3 import user
from openstackclient.tests import fakes
from openstackclient.tests.identity.v3 import fakes as identity_fakes
from openstackclient.tests.identity.v3 import test_identity


class TestUser(test_identity.TestIdentityv3):

    def setUp(self):
        super(TestUser, self).setUp()

        # Get a shortcut to the DomainManager Mock
        self.domains_mock = self.app.client_manager.identity.domains
        self.domains_mock.reset_mock()

        # Get a shortcut to the ProjectManager Mock
        self.projects_mock = self.app.client_manager.identity.projects
        self.projects_mock.reset_mock()

        # Get a shortcut to the RoleManager Mock
        self.roles_mock = self.app.client_manager.identity.roles
        self.roles_mock.reset_mock()

        # Get a shortcut to the UserManager Mock
        self.users_mock = self.app.client_manager.identity.users
        self.users_mock.reset_mock()


class TestUserCreate(TestUser):

    def setUp(self):
        super(TestUserCreate, self).setUp()

        self.domains_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.DOMAIN),
            loaded=True,
        )

        self.projects_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.PROJECT),
            loaded=True,
        )

        self.users_mock.create.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )

        # Get the command object to test
        self.cmd = user.CreateUser(self.app, None)

    def test_user_create_no_options(self):
        arglist = [
            identity_fakes.user_name,
        ]
        verifylist = [
            ('enable', False),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': None,
            'email': None,
            'enabled': True,
            'password': None,
        }

        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)

    def test_user_create_password(self):
        arglist = [
            '--password', 'secret',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('password', 'secret'),
            ('enable', False),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': None,
            'email': None,
            'enabled': True,
            'password': 'secret',
        }
        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)

    def test_user_create_email(self):
        arglist = [
            '--email', 'barney@example.com',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('email', 'barney@example.com'),
            ('enable', False),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': None,
            'email': 'barney@example.com',
            'enabled': True,
            'password': None,
        }
        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)

    def test_user_create_project(self):
        # Return the new project
        self.projects_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.PROJECT_2),
            loaded=True,
        )
        # Set up to return an updated user
        USER_2 = copy.deepcopy(identity_fakes.USER)
        USER_2['project_id'] = identity_fakes.PROJECT_2['id']
        self.users_mock.create.return_value = fakes.FakeResource(
            None,
            USER_2,
            loaded=True,
        )

        arglist = [
            '--project', identity_fakes.PROJECT_2['name'],
            identity_fakes.user_name,
        ]
        verifylist = [
            ('project', identity_fakes.PROJECT_2['name']),
            ('enable', False),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': identity_fakes.PROJECT_2['id'],
            'description': None,
            'domain': None,
            'email': None,
            'enabled': True,
            'password': None,
        }
        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.PROJECT_2['id'],
        )
        self.assertEqual(data, datalist)

    def test_user_create_domain(self):
        arglist = [
            '--domain', identity_fakes.domain_name,
            identity_fakes.user_name,
        ]
        verifylist = [
            ('domain', identity_fakes.domain_name),
            ('enable', False),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': identity_fakes.domain_id,
            'email': None,
            'enabled': True,
            'password': None,
        }
        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)

    def test_user_create_enable(self):
        arglist = [
            '--enable',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('enable', True),
            ('disable', False),
            ('name', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': None,
            'email': None,
            'enabled': True,
            'password': None,
        }
        # UserManager.create(name, domain=, project=, password=, email=,
        #   description=, enabled=, default_project=)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)

    def test_user_create_disable(self):
        arglist = [
            '--disable',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', identity_fakes.user_name),
            ('enable', False),
            ('disable', True),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'default_project': None,
            'description': None,
            'domain': None,
            'email': None,
            'enabled': False,
            'password': None,
        }
        # users.create(name, password, email, tenant_id=None, enabled=True)
        self.users_mock.create.assert_called_with(
            identity_fakes.user_name,
            **kwargs
        )

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)


class TestUserDelete(TestUser):

    def setUp(self):
        super(TestUserDelete, self).setUp()

        # This is the return value for utils.find_resource()
        self.users_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )
        self.users_mock.delete.return_value = None

        # Get the command object to test
        self.cmd = user.DeleteUser(self.app, None)

    def test_user_delete_no_options(self):
        arglist = [
            identity_fakes.user_id,
        ]
        verifylist = [
            ('user', identity_fakes.user_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        self.users_mock.delete.assert_called_with(
            identity_fakes.user_id,
        )


class TestUserList(TestUser):

    def setUp(self):
        super(TestUserList, self).setUp()

        self.domains_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.DOMAIN),
            loaded=True,
        )

        self.projects_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.PROJECT),
            loaded=True,
        )
        self.projects_mock.list.return_value = [
            fakes.FakeResource(
                None,
                copy.deepcopy(identity_fakes.PROJECT),
                loaded=True,
            ),
        ]

        self.roles_mock.list.return_value = [
            fakes.FakeResource(
                None,
                copy.deepcopy(identity_fakes.ROLE),
                loaded=True,
            ),
        ]

        self.users_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )
        self.users_mock.list.return_value = [
            fakes.FakeResource(
                None,
                copy.deepcopy(identity_fakes.USER),
                loaded=True,
            ),
        ]

        # Get the command object to test
        self.cmd = user.ListUser(self.app, None)

    def test_user_list_no_options(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        self.users_mock.list.assert_called_with()

        collist = ('ID', 'Name')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.user_id,
            identity_fakes.user_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_project(self):
        arglist = [
            '--project', identity_fakes.project_id,
        ]
        verifylist = [
            ('project', identity_fakes.project_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        self.users_mock.list.assert_called_with()

        collist = ('ID', 'Name')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.user_id,
            identity_fakes.user_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_domain(self):
        arglist = [
            '--domain', identity_fakes.domain_id,
        ]
        verifylist = [
            ('domain', identity_fakes.domain_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        self.users_mock.list.assert_called_with()

        collist = ('ID', 'Name')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.user_id,
            identity_fakes.user_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_role_user(self):
        arglist = [
            '--role',
            identity_fakes.user_id,
        ]
        verifylist = [
            ('role', True),
            ('user', identity_fakes.user_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'domain': 'default',
            'user': self.users_mock.get(),
        }
        # RoleManager.list(user=, group=, domain=, project=, **kwargs)
        self.roles_mock.list.assert_called_with(
            **kwargs
        )

        collist = ('ID', 'Name')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.role_id,
            identity_fakes.role_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_role_domain(self):
        arglist = [
            '--domain', identity_fakes.domain_name,
            '--role',
            identity_fakes.user_id,
        ]
        verifylist = [
            ('domain', identity_fakes.domain_name),
            ('role', True),
            ('user', identity_fakes.user_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'domain': self.domains_mock.get(),
            'user': self.users_mock.get(),
        }
        # RoleManager.list(user=, group=, domain=, project=, **kwargs)
        self.roles_mock.list.assert_called_with(
            **kwargs
        )

        collist = ('ID', 'Name', 'Domain', 'User')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.role_id,
            identity_fakes.role_name,
            identity_fakes.domain_name,
            identity_fakes.user_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_role_project(self):
        arglist = [
            '--project', identity_fakes.project_name,
            '--role',
            identity_fakes.user_id,
        ]
        verifylist = [
            ('project', identity_fakes.project_name),
            ('role', True),
            ('user', identity_fakes.user_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'project': self.projects_mock.get(),
            'user': self.users_mock.get(),
        }
        # RoleManager.list(user=, group=, domain=, project=, **kwargs)
        self.roles_mock.list.assert_called_with(
            **kwargs
        )

        collist = ('ID', 'Name', 'Project', 'User')
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.role_id,
            identity_fakes.role_name,
            identity_fakes.project_name,
            identity_fakes.user_name,
        ), )
        self.assertEqual(tuple(data), datalist)

    def test_user_list_long(self):
        arglist = [
            '--long',
        ]
        verifylist = [
            ('long', True),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        self.users_mock.list.assert_called_with()

        collist = (
            'ID',
            'Name',
            'Project Id',
            'Domain Id',
            'Description',
            'Email',
            'Enabled',
        )
        self.assertEqual(columns, collist)
        datalist = ((
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
            identity_fakes.domain_id,
            '',
            identity_fakes.user_email,
            True,
        ), )
        self.assertEqual(tuple(data), datalist)


class TestUserSet(TestUser):

    def setUp(self):
        super(TestUserSet, self).setUp()

        self.domains_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.DOMAIN),
            loaded=True,
        )

        self.projects_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.PROJECT),
            loaded=True,
        )

        self.users_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )
        self.users_mock.update.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )

        # Get the command object to test
        self.cmd = user.SetUser(self.app, None)

    def test_user_set_no_options(self):
        arglist = [
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', None),
            ('domain', None),
            ('project', None),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.run(parsed_args)
        self.assertEqual(result, 0)

    def test_user_set_name(self):
        arglist = [
            '--name', 'qwerty',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', 'qwerty'),
            ('password', None),
            ('email', None),
            ('domain', None),
            ('project', None),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
            'name': 'qwerty',
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_password(self):
        arglist = [
            '--password', 'secret',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', 'secret'),
            ('email', None),
            ('domain', None),
            ('project', None),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
            'password': 'secret',
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_email(self):
        arglist = [
            '--email', 'barney@example.com',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', 'barney@example.com'),
            ('domain', None),
            ('project', None),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
            'email': 'barney@example.com',
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_domain(self):
        arglist = [
            '--domain', identity_fakes.domain_id,
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', None),
            ('domain', identity_fakes.domain_id),
            ('project', None),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
            'domainId': identity_fakes.domain_id,
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_project(self):
        arglist = [
            '--project', identity_fakes.project_id,
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', None),
            ('domain', None),
            ('project', identity_fakes.project_id),
            ('enable', False),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
            'projectId': identity_fakes.project_id,
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_enable(self):
        arglist = [
            '--enable',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', None),
            ('domain', None),
            ('project', None),
            ('enable', True),
            ('disable', False),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': True,
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )

    def test_user_set_disable(self):
        arglist = [
            '--disable',
            identity_fakes.user_name,
        ]
        verifylist = [
            ('name', None),
            ('password', None),
            ('email', None),
            ('domain', None),
            ('project', None),
            ('enable', False),
            ('disable', True),
            ('user', identity_fakes.user_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'enabled': False,
        }
        # UserManager.update(user, name=, domain=, project=, password=,
        #     email=, description=, enabled=, default_project=)
        self.users_mock.update.assert_called_with(
            identity_fakes.user_id,
            **kwargs
        )


class TestUserShow(TestUser):

    def setUp(self):
        super(TestUserShow, self).setUp()

        self.users_mock.get.return_value = fakes.FakeResource(
            None,
            copy.deepcopy(identity_fakes.USER),
            loaded=True,
        )

        # Get the command object to test
        self.cmd = user.ShowUser(self.app, None)

    def test_user_show(self):
        arglist = [
            identity_fakes.user_id,
        ]
        verifylist = [
            ('user', identity_fakes.user_id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        self.users_mock.get.assert_called_with(identity_fakes.user_id)

        collist = ('domain_id', 'email', 'enabled', 'id', 'name', 'project_id')
        self.assertEqual(columns, collist)
        datalist = (
            identity_fakes.domain_id,
            identity_fakes.user_email,
            True,
            identity_fakes.user_id,
            identity_fakes.user_name,
            identity_fakes.project_id,
        )
        self.assertEqual(data, datalist)
