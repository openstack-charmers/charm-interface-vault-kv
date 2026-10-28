from unittest import mock

from provides import VaultKVProvides

provider = VaultKVProvides('secrets')

# Only unit_name changed, as when an upgraded client starts sending it.
flags = {'endpoint.secrets.changed.unit_name'}

with mock.patch('provides.is_flag_set', side_effect=flags.__contains__), \
        mock.patch('provides.clear_flag', side_effect=flags.discard), \
        mock.patch('provides.toggle_flag') as toggle_flag, \
        mock.patch.object(VaultKVProvides, 'is_joined',
                          new_callable=mock.PropertyMock,
                          return_value=True):
    provider.manage_flags()

toggle_flag.assert_any_call('endpoint.secrets.new-request', True)
assert not flags, flags
print('unit_name change raises endpoint.secrets.new-request')
