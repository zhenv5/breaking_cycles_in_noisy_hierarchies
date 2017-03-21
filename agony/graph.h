#ifndef GRAPH_H
#define GRAPH_H

#include <stdint.h>
#include <vector>
#include <list>
#include <stdio.h>

#include "queue.h"

class graph {
	public:
		graph() {}

		graph(uint32_t n, uint32_t m) {reset(n, m);}
		graph(const graph & g);

		void reset(uint32_t n, uint32_t m);
		void copy(const graph & g);

		struct edge;

		TAILQ_HEAD(edgelist, edge);

		struct node {
			uint32_t id;
			edgelist out, in;
			uint32_t ind, outd;
		};

		struct edge {
			node *parent, *child;
			uint32_t id;
			bool bound;
			TAILQ_ENTRY(edge) from, to;
		};

		void bind(uint32_t k, uint32_t n, uint32_t m) {bind(getedge(k), getnode(n), getnode(m));}

		void
		bind(edge *e, node *n, node *m)
		{
			TAILQ_INSERT_TAIL(&n->out, e, from);
			TAILQ_INSERT_TAIL(&m->in, e, to);
			n->outd++;
			m->ind++;
			e->bound = true;
			e->parent = n;
			e->child = m;
		}

		void
		unbind(edge *e)
		{
			TAILQ_REMOVE(&e->parent->out, e, from);
			TAILQ_REMOVE(&e->child->in, e, to);
			e->parent->outd--;
			e->child->ind--;
			e->bound = false;
		}

		void
		unbind(node *n)
		{
			while (!TAILQ_EMPTY(&n->out)) unbind(TAILQ_FIRST(&n->out));
			while (!TAILQ_EMPTY(&n->in)) unbind(TAILQ_FIRST(&n->in));
		}

		node * getnode(uint32_t i) {return &m_nodes[i];} 
		edge * getedge(uint32_t i) {return &m_edges[i];} 

	protected:
		const graph & operator = (const graph & ) {return *this;}
		typedef std::vector<node> nodevector;
		typedef std::vector<edge> edgevector;

		nodevector m_nodes;
		edgevector m_edges;
};

class agony
{
	public:

		struct node {
			uint32_t id;
			uint32_t label;

			uint32_t rank;
			uint32_t newrank;
			uint32_t diff;

			node *parent;
			uint32_t paredge;

			uint32_t count;

			TAILQ_ENTRY(node) entries, active;
		};

		TAILQ_HEAD(nodehead, node);

		struct edge {
			bool eulerian;
			uint32_t id;
			uint32_t slack;

			TAILQ_ENTRY(edge) entries;
		};

		TAILQ_HEAD(edgehead, edge);

		uint32_t size() const {return m_nodes.size();}
		node * getnode(uint32_t i) {return &m_nodes[i];} 
		edge * getedge(uint32_t i) {return &m_edges[i];} 

		void cycledfs();

		void initagony();
		void initrank();

		void read(FILE *f);
		void writeagony(FILE *f);

		void relief(uint32_t edge);

		void minagony();

		uint32_t primal() const {return m_primal;}
		uint32_t dual() const {return m_dual;}

		uint32_t cost();


	protected:
		uint32_t slack(node *v, node *u) const {return u->rank > v->rank + 1 ? u->rank - v->rank - 1 : 0;}
		uint32_t newslack(node *v, node *u) const {return u->newrank > v->newrank + 1 ? u->newrank - v->newrank - 1 : 0;}

		uint32_t slack(uint32_t eid) {return slack(from(eid), to(eid));}

		void deleteslack(uint32_t eid);
		void addslack(uint32_t eid);
		
		typedef std::vector<node> nodevector;
		typedef std::vector<edge> edgevector;
		typedef std::vector<nodehead> nodequeue;
		typedef std::vector<edgehead> edgequeue;

		typedef std::list<node *> nodelist;

		void updaterelief(nodelist & nl);
		void resetrelief(nodelist & nl);
		void shiftrank(nodelist & nl, uint32_t s);
		void extractcycle(uint32_t edge);

		node *from(uint32_t eid) {return getnode(m_graph.getedge(eid)->parent->id);}
		node *to(uint32_t eid) {return getnode(m_graph.getedge(eid)->child->id);}


		nodevector m_nodes;
		edgevector m_edges;

		graph m_graph;
		graph m_dag, m_euler;

		edgequeue m_slacks;
		int32_t m_curslack;

		uint32_t m_dual;
		uint32_t m_primal;
		//uint32_t m_minid;
};

#endif
