import fabric.api
from .internals import (
    wrapExpectations,
    wrapExpectationsLocal,
    ExpectationContext,
)


def expect(prompt, response, exit_after=None, hide_input=False):
    """Return an expectation structure.

    :Params:
        - `prompt`: the speicic prompt we're looking for
        - `response`: the response to give
        - `exit_after`: number of seconds we should exit after
        - `hide_input`: boolean for whether or not we should hide the input

    """
    return [
        {
            'prompt': prompt,
            'response': response,
            'exit_after': exit_after,
            'hide_input': hide_input,
        }
    ]

def expecting(e):
    return ExpectationContext(e)

def run(cmd, **kwargs):
    #run wrapper 
    tmp_file = None
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd, tmp_file = wrapExpectations(cmd)
    result = fabric.api.run(cmd, **kwargs)
    if tmp_file:
        fabric.api.run('rm %s' % (tmp_file,))
    return result

def sudo(cmd, **kwargs):
    #sudo wrapper
    tmp_file = None
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd, tmp_file = wrapExpectations(cmd)

    result = fabric.api.sudo(cmd, **kwargs)
    if tmp_file:
        fabric.api.sudo('rm %s' % (tmp_file,))
    return result

def local(cmd, **kwargs):
    #local wrapper
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd = wrapExpectationsLocal(cmd)
    return fabric.api.local(cmd, **kwargs)

