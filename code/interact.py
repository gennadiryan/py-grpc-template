def get_input(prompt, options):
    split_input = lambda s: (s.split(' ')[:2], ' '.join(s.split(' ')[2:]))
    args, value = split_input(input(prompt))
    while len(args) == 0 or args[0] not in options:
        print('Invalid command')
        args, value = split_input(input(prompt))
    return args, value

def keyvaluestore_prompt(prompt):
    options = 'get put delete exit'.split()
    args, value = get_input(prompt, options)
    while args[0] != 'exit':
        if len(args) != 2:
            print(f'No key supplied for command {args[0]}')
        else:
            yield args[0], args[1], value
        args, value = get_input(prompt, options)
    yield None

if __name__ == '__main__':
    generator = keyvaluestore_prompt('>>> ')
    result = next(generator)
    while result is not None:
        command, key, value = result
        if command == 'get':
            print(f'Getting key "{key}"')
        elif command == 'put':
            print(f'Putting key "{key}" with value "{value}"')
        elif command == 'delete':
            print(f'Deleting key "{key}"')
        else:
            print(f'Invalid command "{command}"; exiting')
            break
        result = next(generator)
