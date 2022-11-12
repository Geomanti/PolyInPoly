import matplotlib.pyplot as plt
import math as m
from shapely import geometry as g

# Cleaning data before using


def PointsToPolygon(text):
	temp1 = text.replace('(', '')
	context = temp1.replace(')', '')
	wordFree = context.replace('POLYGON', '')
	Emptytext = wordFree.replace('Polygon', '')
	context = Emptytext.replace('GEOMETRYCOLLECTION', '')
	wordFree = context.replace('EMPTY', '')
	points = wordFree.split(',')
	polygonlist = list()

	for i in points:
		point = list()
		coordinates = i.split(' ')

		for coord in coordinates:

			if coord == '':
				continue

			value = float(coord)
			point.append(value)

		polygonlist.append(point)
	return polygonlist

# Creating coords for contour to visualize with matplotlib


def ShapeToViewContour(polygon):
	x = []
	y = []
	rings = list()
	exterior = list(polygon.exterior.coords)
	rings.append(exterior)

	try:
		interior = list(polygon.interior.coords)
		rings.append(interior)
	except:print('No interior found')

	for element in rings:

		for point in element:
			x.append(point[0])
			y.append(point[1])

		plt.plot(x, y, 'r')

# Creating coords for polygon to visualize with matplotlib


def ShapeToView(pointlist):
	x = []
	y = []

	for point in pointlist:
		x.append(point[0])
		y.append(point[1])

	plt.fill(x, y)

# Funtion to find intersections with second poly and
# Creating transform vectors for scaling
# and also write intersection as index of poly 1


def InterPoints(poly1, poly2, interior):
	polygon1 = g.Polygon(poly1)
	movevector = list()
	interlist = list()
	intersectindex = list()
	plusindex = 0

	# Getting through poly1 points
	for index1 in range(len(poly1)):

		# getting through poly2 points to find intersections
		intermin = 0
		intermax = 0
		intersect = 0
		stopper = 0
		pointsmin = list()
		pointsmax = list()
		trvector = list()
		for index2 in range(len(poly2)):

			# Ensure that that index in range
			if index1+1 < len(poly1):
				plusindex = index1 + 1
			else:
				plusindex = 1
			if index1-1 == -1:
				minusindex = -2
			else:
				minusindex = index1-1

			# Checking intersections
			if ((float(poly1[index1][0]) == float(poly2[index2][0]))
			and (float(poly1[index1][1]) == float(poly2[index2][1]))):
				interlist.append(poly1[index1])

				if index1 in intersectindex:
					pass
				else:
					intersectindex.append(index1)

				intersect = 1

				# Cheking previous point for intersection
			if ((float(poly1[minusindex][0]) == float(poly2[index2][0]))
			and (float(poly1[minusindex][1]) == float(poly2[index2][1]))):
				intermin = 1
				pointsmin.append(poly1[minusindex])

			# Cheking next point for intersection
			if ((float(poly1[plusindex][0]) == float(poly2[index2][0]))
			and (float(poly1[plusindex][1]) == float(poly2[index2][1]))):
				intermax = 1
				pointsmax.append(poly1[plusindex])

		if ((intermin == 1) and (intermax == 1)) and (intersect == 1):

			# Getting middle point between 2 points
			stopper = 1
			pmin = pointsmin[0]
			pmax = pointsmax[0]
			midpoint = list()
			midpoint = MidPoint(pmin, pmax)
			checkpoint = g.Point(midpoint[0], midpoint[1])

			# Creating transformation vector
			if polygon1.contains(checkpoint):

				if interior == 0:
					trvector = Vec2pt(midpoint, poly1[index1])
				else:
					trvector = Vec2pt(poly1[index1], midpoint)

				movevector.append(trvector)
			else:

				if interior == 0:
					trvector = Vec2pt(poly1[index1], midpoint)
				else:
					trvector = Vec2pt(midpoint, poly1[index1])

				movevector.append(trvector)
		if (((intermin == 1) or (intermax == 1))
		and (intersect == 1) and (stopper == 0)):

			if intermax == 1:

				if interior == 0:
					trvector = Vec2pt(poly1[minusindex], poly1[index1])
				else:
					trvector = Vec2pt(poly1[index1], poly1[minusindex])

				movevector.append(trvector)
			else:

				if interior == 0:
					trvector = Vec2pt(poly1[plusindex], poly1[index1])
				else:
					trvector = Vec2pt(poly1[index1], poly1[plusindex])

				movevector.append(trvector)

	# To adjust polygon later with movevectors
	interlist.append(intersectindex)
	interlist.append(movevector)
	return interlist

# Simple function to create vector from 2 points


def Vec2pt(point1, point2):
	xm = point2[0]
	ym = point2[1]
	xs = point1[0]
	ys = point1[1]
	xv = xm-xs
	yv = ym-ys
	mg = m.sqrt(xv**2 + yv**2)

	if (xv == 0) and (yv == 0):
		xv = xm - xs*0.99999
		yv = ym - ys*0.99999
		mg = m.sqrt(xv**2 + yv**2)

	vector = list()
	vector.append(xv/mg)
	vector.append(yv/mg)
	return vector

# Function to transform poly1 points by indexs of intersection with poly2 by transform vectors


def PointsXVectors(polygon, intersectindexs, vectorlist):
	polypoint = list()
	TransformedPoly = list()

	for index1 in range(len(polygon)):
		cpoint = list()
		cpoint = polygon[index1]

		for index2 in range(len(intersectindexs)):

			if index1 == intersectindexs[index2]:
				polypoint = polygon[index1]
				vector = vectorlist[index2]
				cpoint = list()
				x = polypoint[0] + vector[0]
				y = polypoint[1] + vector[1]
				cpoint.append(x)
				cpoint.append(y)

		TransformedPoly.append(cpoint)

	return TransformedPoly

# Function to extend list


def AddPoints(pointlist1, pointlist2):
	newlist = list()
	newlist.append(pointlist1[0])

	for point in pointlist2:
		newlist.append(point)

	for index in range(len(pointlist1)):
		newlist.append(pointlist1[len(pointlist1)-index-1])

	return newlist

# Simple function to scale vectors to get desirable area


def Scaletofitspace(pointlist, vectorlist, value):
	polygon = g.Polygon(pointlist)
	scalar = value / polygon.area
	newvectorlist = list()
	newvector = list()

	for vector in vectorlist:
		x = vector[0] * scalar
		y = vector[1] * scalar
		newvector.append(x)
		newvector.append(y)
		newvectorlist.append(newvector)
		newvector = list()

	return newvectorlist

# Complex function to scale vectors to get desirable area


def ScaleVtoFitA(points, pointstransformed, vectorlist, refpoly, value):
	polygonoptimized = g.Polygon(points)
	polygontransformed = g.Polygon(pointstransformed).convex_hull
	refpoly1 = g.Polygon(refpoly)
	scalar = ((refpoly1.area + value - polygonoptimized.area) /
			(polygontransformed.area - polygonoptimized.area))
	newvectorlist = list()
	newvector = list()

	for vector in vectorlist:
		x = vector[0] * scalar
		y = vector[1] * scalar
		newvector.append(x)
		newvector.append(y)
		newvectorlist.append(newvector)
		newvector = list()

	return newvectorlist

# Function to find middle point between 2 points


def MidPoint(point1, point2):
	x1 = point1[0]
	y1 = point1[1]
	x2 = point2[0]
	y2 = point2[1]
	xmid = (x1+x2)/2
	ymid = (y1+y2)/2
	middlepoint = list()
	middlepoint.append(xmid)
	middlepoint.append(ymid)
	return middlepoint

# Just like convex hull function but you can adjust it and it only removes points that intersects


def Optimization(poly1, poly2, fillholes, simplify):
	polygon1 = g.Polygon(poly1)
	scale = simplify / 100
	bufferparam = (polygon1.area / 100) * scale
	coordinates1 = list()

	try:
		exterior = list(polygon1.exterior.coords)
		coordinates1.append(exterior)
	except:
		print('Failed to optimize exterior ring of first polygon')

	try:

		if fillholes:
			pass
		else:
			interior = list(polygon1.interior.coords)
			coordinates1.append(interior)

	except:
		print('Failed to optimize interior ring of first polygon')

	inter = 0
	newpolycoords = list()
	newring = list()
	for rings in coordinates1:

		for index1 in range(len(rings)):
			intermin = 0
			intermax = 0
			intersect = 0
			stopper = 0
			pointsmin = list()
			pointsmax = list()
			skip = False

			for index2 in range(len(poly2)):

				if index1+1 < len(rings):
					plusindex = index1 + 1
				else:
					plusindex = 1

				if index1-1 == -1:
					minusindex = -2
				else:
					minusindex = index1-1

				if ((float(rings[index1][0]) == float(poly2[index2][0]))
				and (float(rings[index1][1]) == float(poly2[index2][1]))):
					intersect = 1

				if ((float(rings[minusindex][0]) == float(poly2[index2][0]))
				and (float(rings[minusindex][1]) == float(poly2[index2][1]))):
					intermin = 1
					pointsmin.append(rings[minusindex])

				if ((float(rings[plusindex][0]) == float(poly2[index2][0]))
				and (float(rings[plusindex][1]) == float(poly2[index2][1]))):
					intermax = 1
					pointsmax.append(rings[plusindex])

				if (((intermin == 1) and (intermax == 1))
				and (intersect == 1) and (stopper == 0)):
					stopper = 1
					pmin = pointsmin[0]
					pmax = pointsmax[0]
					midpoint = list()
					midpoint = MidPoint(pmin, pmax)
					vector = Vec2pt(rings[index1], midpoint)
					x = vector[0] + rings[index1][0]
					y = vector[1] + rings[index1][1]
					line = list()
					line.append(pmin)
					line.append(pmax)
					checkpoint = g.Point(x, y)
					linestring = g.LineString(line).buffer(bufferparam, cap_style=2)

					if polygon1.contains(checkpoint):

						if inter == 0:
							pass
						else:
							skip = True

					else:
						skip = True

					if linestring.contains(g.Point(rings[index1][0], rings[index1][1])):
						skip = True

			if skip:
				pass
			else:
				newring.append(list(rings[index1]))

		newpolycoords.append(newring)
		inter = 1

	return newpolycoords

# Convex Hull function to remove intersecting points


def smartConvex(polypoints, intersectindexs, usefultrvectors, inter):
	convexpoly = g.Polygon(polypoints).convex_hull.buffer(-10, join_style=2)
	newpoly = list()
	newindexs = list()
	newvectors = list()
	newvectors.extend(usefultrvectors)

	for index1 in range(len(polypoints)):
		skip = False

		for index2 in intersectindexs:

			if index1 == index2:
				point = polypoints[index1]
				checkpoint = g.Point(point[0], point[1])

				if convexpoly.contains(checkpoint):

					if inter == 0:
						skip = True
						newvectors.pop(0)
					else:
						newindexs.append(index2)

				else:
					if inter == 1:
						skip = True
						newvectors.pop(0)

					newindexs.append(index2)

		if skip:
			pass
		else:
			newpoly.append(polypoints[index1])

	newpoly.append(newvectors)
	newpoly.append(newindexs)
	return newpoly

# Function to assamble all the small functions


def ExtendPolyintoPoly2(polypoints1, polypoints2, trvalue, fillholes, simplify):
	print('Optimizing plygon')
	optimizedpoly = Optimization(polypoints1, polypoints2, fillholes, simplify)
	inter = 0
	newpoly = list()
	print('Finding intersections')

	for element in optimizedpoly:
		intersectpoints = InterPoints(element, polypoints2, inter)
		transformvectors = intersectpoints.pop()
		intersectindexs = intersectpoints.pop()

		# First transform and correction
		transformedpoints = PointsXVectors(element, intersectindexs, transformvectors)
		usefultrvectors = ScaleVtoFitA(element, transformedpoints, transformvectors, polypoints1, trvalue)
		transformedpoints1 = PointsXVectors(element, intersectindexs, usefultrvectors)
		removedinsidepoints = smartConvex(transformedpoints1, intersectindexs, usefultrvectors, inter)

		# After smart Convex code removes some points, vectors and indexs
		newinterindexs = removedinsidepoints.pop()
		newvectors = removedinsidepoints.pop()

		# Second transform and correction after smart Convex
		transformedpoints2 = PointsXVectors(removedinsidepoints, newinterindexs, newvectors)
		newusefulvectors = ScaleVtoFitA(removedinsidepoints, transformedpoints2, newvectors, polypoints1, trvalue)
		transformedpoints3 = PointsXVectors(removedinsidepoints, newinterindexs, newusefulvectors)
		inter = 1
		newpoly.append(transformedpoints3)
	return newpoly
