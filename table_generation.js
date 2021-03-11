const heading = {a: "A", b: "B"}
const data = [{a: "T", b: "F"}, {a: "F", b: "F"}]

var t = d3.select('body').append('table')

t
	.append('thead')
	.append('tr')
	.selectAll('th')
	.data(Object.values(heading))
	.enter()
	.append('th')
	.text(data => data)

var rows = t.append('tbody').selectAll('tr')
	.data(data)
	.enter()
	.append('tr')

var cells = rows.selectAll('td')
	.data(d => Object.values(d))
	.enter()
	.append("td")
		.text(d => d);
