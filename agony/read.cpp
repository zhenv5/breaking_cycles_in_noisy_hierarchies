#include "graph.h"
#include <map>

typedef std::map<uint32_t, uint32_t> intmap;

void
agony::read(FILE *f)
{
	uint32_t cnt = 0;
	uint32_t a, b;
	uint32_t ecnt = 0;

	intmap labelmap;



	while (fscanf(f, "%d%d", &a, &b) == 2) {
		if (labelmap.count(a) == 0)
			labelmap[a] = cnt++;
		if (labelmap.count(b) == 0)
			labelmap[b] = cnt++;
		ecnt++;
	}

	m_nodes.resize(cnt);
	m_edges.resize(ecnt);

	for (uint32_t i = 0; i < size(); i++)
		m_nodes[i].id = i;

	for (intmap::iterator it = labelmap.begin(); it != labelmap.end(); ++it)
		m_nodes[it->second].label = it->first;

	for (uint32_t i = 0; i < m_edges.size(); i++)
		m_edges[i].id = i;

	m_graph.reset(cnt, ecnt);

	rewind(f);

	ecnt = 0;
	while (fscanf(f, "%d%d", &a, &b) == 2) {
		m_graph.bind(ecnt, labelmap[a], labelmap[b]);
		ecnt++;
	}
}

void
agony::writeagony(FILE *f)
{
	intmap ranks;

	for (uint32_t i = 0; i < size(); i++) {
		ranks[m_nodes[i].rank] = 0;
	}

	uint32_t r = 0;
	for (intmap::iterator it = ranks.begin(); it != ranks.end(); ++it)
		it->second = r++;

	for (uint32_t i = 0; i < size(); i++) {
		fprintf(f, "%d %d\n", m_nodes[i].label, ranks[m_nodes[i].rank]);
	}

}
