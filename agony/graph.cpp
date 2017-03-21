#include "graph.h"
#include <assert.h>

void
graph::reset(uint32_t n, uint32_t m) 
{
	m_nodes.resize(n);
	m_edges.resize(m);

	for (uint32_t i = 0; i < n; i++) {
		TAILQ_INIT(&m_nodes[i].out);
		TAILQ_INIT(&m_nodes[i].in);
		m_nodes[i].id = i;
		m_nodes[i].ind = m_nodes[i].outd = 0;
	}

	for (uint32_t i = 0; i < m_edges.size(); i++) {
		m_edges[i].id = i;
		m_edges[i].bound = false;
	}
}


graph::graph(const graph & g) {copy(g);}

void
graph::copy(const graph & g)
{
	reset(g.m_nodes.size(), g.m_edges.size());

	for (uint32_t i = 0; i < m_edges.size(); i++) {
		if (g.m_edges[i].bound)
			bind(i, g.m_edges[i].parent->id, g.m_edges[i].child->id);
	}

}

uint32_t
agony::cost()
{
	uint32_t t = 0;

	for (uint32_t i = 0; i < m_edges.size(); i++) {
		node *n = from(i);
		node *m = to(i);
		if (m->rank <= n->rank) t += n->rank - m->rank + 1;

	}

	return t;
}


void
agony::cycledfs()
{
	graph dfs(m_graph);


	nodehead active;
	TAILQ_INIT(&active);

	for (uint32_t i = 0; i < size(); i++) TAILQ_INSERT_TAIL(&active, &m_nodes[i], entries);

	while (!TAILQ_EMPTY(&active)) {
		node *seed = TAILQ_FIRST(&active);
		node *u = seed;

		u->parent = 0;
		
		while (u) {

			graph::node *n = dfs.getnode(u->id);
			if (TAILQ_EMPTY(&n->out)) {
				TAILQ_REMOVE(&active, u, entries);	
				dfs.unbind(n);
				u = u->parent;
			}
			else {
				graph::edge *e = TAILQ_FIRST(&n->out);
				graph::node *m = e->child;
				node *v = getnode(m->id);

				if (v->parent == 0 && v != seed) {
					v->parent = u;
					v->paredge = e->id;
					u = v;
				}
				else {
					for (node *w = u; w != v; w = w->parent) {
						getedge(w->paredge)->eulerian = true;
						dfs.unbind(dfs.getedge(w->paredge));
					}

					getedge(e->id)->eulerian = true;
					dfs.unbind(e);

					for (node *w = u, *wnext; w != v; w = wnext) {
						wnext = w->parent;
						w->parent = 0;
					}

					u = v;
				}
			}
		}
	}
}

void
agony::initagony()
{
	m_dag.copy(m_graph);
	m_euler.copy(m_graph);

	for (uint32_t i = 0; i < m_edges.size(); i++) {
		if (getedge(i)->eulerian) {
			m_dag.unbind(m_dag.getedge(i));
			m_dual++;
		}
		else {
			m_euler.unbind(m_euler.getedge(i));
		}
	}

	m_primal = m_dual;
}

void
agony::initrank()
{
	nodelist sources;

	for (uint32_t i = 0; i < size(); i++) {
		node *n = getnode(i);
		n->count = m_dag.getnode(i)->ind;
		if (n->count == 0) {
			n->newrank = n->rank = 0;
			sources.push_back(n);
		}
	}

	while (!sources.empty())  {
		node *n = sources.front();
		sources.pop_front();

		graph::node *u = m_dag.getnode(n->id);
		graph::edge *e;
		TAILQ_FOREACH(e, &u->out, from) {
			node *m = getnode(e->child->id);
			m->count--;
			m->newrank = m->rank = std::max(m->rank, n->rank + 1);
			if (m->count == 0) sources.push_back(m);
		}
	}

	m_slacks.resize(size());
	for (uint32_t i = 0; i < size(); i++) {
		TAILQ_INIT(&m_slacks[i]);
	}

	m_curslack = -1;
	for (uint32_t i = 0; i < m_edges.size(); i++) {
		if (getedge(i)->eulerian) addslack(i);
		m_curslack = std::max(int32_t(slack(i)), m_curslack);
	}
}

void
agony::minagony()
{
	for (uint32_t i = 0; i < size(); i++) {
		graph::node *n = m_dag.getnode(i);
		graph::edge *e;

		TAILQ_FOREACH(e, &n->out, from) {
			assert(from(e->id)->rank < to(e->id)->rank);
		}
	}

	while(true) {
		while (m_curslack >= 0 && TAILQ_EMPTY(&m_slacks[m_curslack])) m_curslack--;
		if (m_curslack < 0) break;

		edge *e = TAILQ_FIRST(&m_slacks[m_curslack]);

		relief(e->id);	
		printf("%d %d\n", primal(), dual());
	}
}


void
agony::relief(uint32_t edge)
{
	graph::edge *e = m_euler.getedge(edge);
	node *p = getnode(e->parent->id);
	node *s = getnode(e->child->id);

	p->parent = 0;
	p->diff = slack(p, s);
	assert(p->diff > 0);

	// Add and init queue
	nodequeue q(p->diff);
	for (uint32_t i = 0; i < q.size(); i++)
		TAILQ_INIT(&q[i]);
	TAILQ_INSERT_TAIL(&q[p->diff - 1], p, entries);
	int32_t curstack = p->diff - 1;

	nodelist nl;
	nodelist visited;
	nl.push_back(p);

	uint32_t bound = 0;

	while (true) {

		while (curstack >= 0 && TAILQ_EMPTY(&q[curstack])) curstack--;

		if (curstack < int32_t(bound)) {
			break;
		}

		node *u = TAILQ_FIRST(&q[curstack]);
		TAILQ_REMOVE(&q[curstack], u, entries);



		u->newrank = u->rank + u->diff;
		visited.push_back(u);
		u->diff = 0; // diff = 0 means that u is no longer in the stack

		if (u == s) break;

		graph::node *n = m_dag.getnode(u->id);

		TAILQ_FOREACH(e, &n->out, from) {
			node *v = getnode(e->child->id);
			assert(u->rank < v->rank);
			if (v->newrank <= u->newrank) {
				uint32_t t = u->newrank + 1 - v->newrank;
				assert(t - 1 <= curstack);
				if (v == s) bound = std::max(bound, t);
				if (t > v->diff) {
					if (v->diff > 0) TAILQ_REMOVE(&q[v->diff - 1], v, entries);
					else nl.push_back(v);
					v->diff = t;
					// add v to queue
					TAILQ_INSERT_TAIL(&q[v->diff - 1], v, entries);
					v->parent = u;
					v->paredge = e->id;
				}
			}
		}

		n = m_euler.getnode(u->id);
		TAILQ_FOREACH(e, &n->in, to) {
			node *v = getnode(e->parent->id);
			if (newslack(v, u) > slack(v, u)) {
				uint32_t t = newslack(v, u) - slack(v, u);
				assert(t - 1 <= curstack);
				if (v == s) bound = std::max(bound, t);
				if (t > v->diff) {
					if (v->diff > 0) TAILQ_REMOVE(&q[v->diff - 1], v, entries);
					else nl.push_back(v);
					v->diff = t;
					// add v to queue
					TAILQ_INSERT_TAIL(&q[v->diff - 1], v, entries);
					v->parent = u;
					v->paredge = e->id;
				}
			}
		}

	}

	if (curstack >= 0) shiftrank(visited, curstack + 1);
		
	updaterelief(nl);
	if (slack(p, s)) extractcycle(edge);

}

void
agony::updaterelief(nodelist & nl)
{
	for (nodelist::iterator it = nl.begin(); it != nl.end(); ++it) {
		node *n = *it;
		n->rank = n->newrank;
		n->diff = 0;
	}

	for (nodelist::iterator it = nl.begin(); it != nl.end(); ++it) {
		node *u = *it;
		graph::edge *e;
		graph::node *n = m_euler.getnode(u->id);
		TAILQ_FOREACH(e, &n->out, from) {
			node *v = to(e->id);
			edge *f = getedge(e->id);
			if (slack(u, v) != f->slack) {
				deleteslack(e->id);
				addslack(e->id);
			}
		}
	}
}

void
agony::resetrelief(nodelist & nl)
{
	for (nodelist::iterator it = nl.begin(); it != nl.end(); ++it) {
		node *n = *it;
		n->newrank = n->rank;
		n->diff = 0;
	}
}

void
agony::shiftrank(nodelist & nl, uint32_t shift)
{
	for (nodelist::iterator it = nl.begin(); it != nl.end(); ++it) {
		node *n = *it;
		n->newrank -= shift;
	}
}

void
agony::extractcycle(uint32_t eid)
{
	graph::edge *e = m_euler.getedge(eid);
	node *p = getnode(e->parent->id);
	node *s = getnode(e->child->id);

	for (node *u = s; u != p; u = u->parent) {

		edge *f =  getedge(u->paredge);

		if (f->eulerian) {
			f->eulerian = false;
			m_euler.unbind(m_euler.getedge(u->paredge));
			assert(u->rank < u->parent->rank);
			m_dag.bind(u->paredge, u->id, u->parent->id);
			deleteslack(u->paredge);
			m_dual--;
			m_primal--;
		}
		else {
			f->eulerian = true;
			m_dag.unbind(m_dag.getedge(u->paredge));
			m_euler.bind(u->paredge, u->parent->id, u->id);
			addslack(u->paredge);
			m_dual++;
			m_primal++;
		}
	}

	edge *g = getedge(eid);

	g->eulerian = false;
	m_euler.unbind(e);
	m_dag.bind(eid, p->id, s->id);
	m_dual--;
	m_primal--;
	deleteslack(eid);
}

void
agony::deleteslack(uint32_t eid)
{
	uint32_t t = getedge(eid)->slack;
	if (t > 0) TAILQ_REMOVE(&m_slacks[t - 1], getedge(eid), entries);
	m_primal -= t;
}

void
agony::addslack(uint32_t eid)
{
	uint32_t t = slack(eid);
	edge *e = getedge(eid);
	e->slack = t;
	if (t > 0) TAILQ_INSERT_TAIL(&m_slacks[t - 1], getedge(eid), entries);
	m_primal += t;
}
