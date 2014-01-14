import fabric.api
from ilogue.fexpect.internals import wrapExpectations, wrapExpectationsLocal, ExpectationContext


def expect(promptexpr, response, exitAfter=-1):
    if not exitAfter == -1:
        return [(promptexpr, response, exitAfter)]
    return [(promptexpr, response)]

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

