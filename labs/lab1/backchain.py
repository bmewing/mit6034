from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES
from pprint import pprint

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def matcher(rule, statement):
    consequent = rule.consequent()
    return match(consequent[0], statement) is not None


def backchain_to_goal_tree(rules, hypothesis):
    output = OR(hypothesis)
    matches = [populate(r.antecedent(), match(r.consequent()[0], hypothesis)) for r in rules if matcher(r, hypothesis)]
    if len(matches) > 0:
        for m in matches:
            if isinstance(m, AND):
                to_append = AND()
            else:
                to_append = OR()
            if not isinstance(m, (AND, OR)):
                m = AND(m)
            for a in m:
                child_append = OR(a)
                child_append.append(backchain_to_goal_tree(rules, a))
                to_append.append(child_append)
            output.append(to_append)
    else:
        output.append(OR())
    return simplify(output)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print(backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin'))
