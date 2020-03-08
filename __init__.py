import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from distutils.sysconfig import get_python_lib
import matplotlib as mpl



class Crust1p0(object):
	"""docstring for Crust1p0"""
	def __init__(self, reread = False):
		if reread:
			read_db()
		self.data = pickle.load(open('/home/anis/GitHub/CRUST1p0/crust1p0.pkl', 'rb'))

	def gen_raster(self):
		lon = np.arange(-89.5,89.5+1,1.0)
		lat = np.arange(-179.5,179.5+1,1.0)
		lonXX,latYY = np.meshgrid(lon,lat)
		for i in range(np.shape(lonXX)[0]):
			for j in range(np.shape(lonXX)[1]):
				bounds, Vp, Vs, Rho = self.point(latYY[i,j],lonXX[i,j])

	def gen_regional_map(self,m,min_lat,max_lat,min_lon,max_lon,\
		map = 'crustal_thickness'):
		min_lat = max(-89.5,np.floor(min_lat/0.5)*0.5)
		max_lat = min(89.5,np.ceil(max_lat/0.5)*0.5)
		min_lon = max(-179.5,np.floor(min_lon/0.5)*0.5)
		max_lon = min(179.5,np.ceil(max_lon/0.5)*0.5)
		lat = np.arange(min_lat,max_lat+1,1.0)
		lon = np.arange(min_lon,max_lon+1,1.0)
		lonXX,latYY = np.meshgrid(lon,lat)
		crustal_thick = np.zeros(np.shape(lonXX))
		water_thick = np.zeros(np.shape(lonXX))
		ice_thick = np.zeros(np.shape(lonXX))
		upper_sediment = np.zeros(np.shape(lonXX))
		middle_sediment = np.zeros(np.shape(lonXX))
		lower_sediment = np.zeros(np.shape(lonXX))
		upper_crust = np.zeros(np.shape(lonXX))
		middle_crust = np.zeros(np.shape(lonXX))
		lower_crust = np.zeros(np.shape(lonXX))
		for i in range(np.shape(lonXX)[0]):
			for j in range(np.shape(lonXX)[1]):
				bounds, Vp, Vs, Rho = self.point(latYY[i,j],lonXX[i,j])
				crustal_thick[i,j] = bounds[0]-bounds[-1]
				water_thick[i,j] = bounds[0] - bounds[1]
				ice_thick[i,j] = bounds[1] - bounds[2]
				upper_sediment[i,j] = bounds[2] - bounds[3]
				middle_sediment[i,j] = bounds[3] - bounds[4]
				lower_sediment[i,j] = bounds[4] - bounds[5]
				upper_crust[i,j] = bounds[5] - bounds[6]
				middle_crust[i,j] = bounds[6] - bounds[7]
				lower_crust[i,j] = bounds[7] - bounds[8]
		if map == 'crustal thickness':
			m.contourf(lonXX,latYY, crustal_thick,cmap=plt.get_cmap('rainbow'))
		elif map == 'ice thickness':
			m.contourf(lonXX,latYY, ice_thick,cmap=plt.get_cmap('Blues'))
		elif map == 'water depth':
			m.contourf(lonXX,latYY, water_thick,cmap=plt.get_cmap('Blues'))
		elif map == 'upper sediment':
			m.contourf(lonXX,latYY, upper_sediment,cmap=plt.get_cmap('rainbow'))
		elif map == 'middle sediment':
			m.contourf(lonXX,latYY, middle_sediment,cmap=plt.get_cmap('rainbow'))
		elif map == 'lower sediment':
			m.contourf(lonXX,latYY, lower_sediment,cmap=plt.get_cmap('rainbow'))
		elif map == 'upper crust':
			m.contourf(lonXX,latYY, upper_crust,cmap=plt.get_cmap('rainbow'))
		elif map == 'middle crust':
			m.contourf(lonXX,latYY, middle_crust,cmap=plt.get_cmap('rainbow'))
		elif map == 'lower crust':
			m.contourf(lonXX,latYY, lower_crust,cmap=plt.get_cmap('rainbow'))
		m.colorbar(location='right')
		
	def gen_all_regional_maps(self,min_lat,max_lat,min_lon,max_lon,\
			fname='./figs/sample_'):
		map_items = ['crustal thickness', 'ice thickness', 'water depth',\
			'upper sediment', 'middle sediment', 'lower sediment',\
			'upper crust', 'middle crust', 'lower crust']
		for item in map_items:
			plt.close('all')
			from mpl_toolkits.basemap import Basemap
			import matplotlib.cm as cm
			fig = plt.figure(figsize=(30,20))
			m = Basemap(width=800000000,height=700000000)
			m.drawparallels(np.arange(-90,90,20),labels=[True])
			m.drawmeridians(np.arange(-180,180,20),labels=[False,True,True,False], rotation=90)
			m.drawcountries()
			m.drawcoastlines()
			self.gen_regional_map(m,min_lat,max_lat,min_lon,max_lon,\
				map = item)
			plt.title(item)
			plt.savefig(fname+item+'.png',bbox_inches = 'tight',pad_inches = 0)
	def gen_all_global_map(self):
		self.gen_all_regional_maps(-89.5,89.5,-179.5,179.5)
	def gen_global_map(self,m):
		self.gen_regional_map(m,-89.5,89.5,-179.5,179.5)

	def plot_crust_at_point(self,ax,lat,lon):
		bounds, Vp, Vs, Rho = self.point(lat,lon)
		colors = ['b','c','gold','orange','darkorange','lightcoral','coral','red','brown']
		legends = ['water','ice','upper sediments','middle sediments',\
		'lower sediments','upper crystalline crust','middle crystalline crust',\
		'lower crystalline crust', 'mantle']
		str_fmt = r'v_s = {0:7.2f} km, v_p = {1:7.2f} km, v_s = {2:7.2f} tons/m^3'
		for i,bound in enumerate(bounds):
			ax.axhline(bound,0,100, c='k', lw=0.5)
			if i == (len(bounds)-1):
				ax.fill_between([0.0,100.0],bound,bound-10,\
					color=colors[i],label=legends[i])
				thick = True
			else:
				ax.fill_between([0.0,100.0],bound,bounds[i+1],\
					color=colors[i],label=legends[i])
				if abs(bound - bounds[i+1])>0.0:
					thick = True
				else:
					thick = False
			if thick:
				string = str_fmt.format(Vs[i],Vp[i],Rho[i])
				ax.text(50.0,bound,string,ha='center',va='top')
		ax.set_yticks(ticks=bounds)
		ax.set_ylabel('depth (km)')
		ax.set_title('Crustal Layer at Lat {0:5.2f} Lon {1:5.2f}'.format(lat,lon))
		ax.legend()

	def cross_section(self,point1,point2,dL=0.05,size=(15,5)):
		"""
		para point1: (lon,lat)
		type point1: list
		para point2: (lon,lat)
		type point2: list
		"""
		fig = plt.figure(figsize=size)
		ax = plt.gca()
		fake_length = np.sqrt(\
			(point2[1]-point1[1])**2 + (point2[0]-point1[0])**2 )
		n = int(np.ceil(fake_length/dL))
		dL = fake_length/n
		slope = (np.array(point2) - np.array(point1))/fake_length
		xaxis = np.linspace(0,fake_length,n)
		cmap = mpl.cm.get_cmap('viridis')
		norm = mpl.colors.Normalize(vmin=0, vmax=10)
		for i in range(n+1):
			loc = point1 + (i+0.5)*dL*slope
			bounds, Vp, Vs, Rho = self.point(loc[0],loc[1])
			plt.plot([i*dL,(i+1)*dL],[bounds[0],bounds[0]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[1],bounds[1]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[2],bounds[2]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[3],bounds[3]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[4],bounds[4]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[5],bounds[5]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[6],bounds[6]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[7],bounds[7]], c='k', lw=0.5)
			plt.plot([i*dL,(i+1)*dL],[bounds[8],bounds[8]], c='k', lw=0.5)
			plt.fill_between([i*dL,(i+1)*dL],bounds[0],bounds[1],color='b')
			plt.fill_between([i*dL,(i+1)*dL],bounds[1],bounds[2],color='c')
			plt.fill_between([i*dL,(i+1)*dL],bounds[2],bounds[3],color=cmap(norm(Vs[2])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[3],bounds[4],color=cmap(norm(Vs[3])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[4],bounds[5],color=cmap(norm(Vs[4])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[5],bounds[6],color=cmap(norm(Vs[5])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[6],bounds[7],color=cmap(norm(Vs[6])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[7],bounds[8],color=cmap(norm(Vs[7])))
			plt.fill_between([i*dL,(i+1)*dL],bounds[8],bounds[8]-10,color=cmap(norm(Vs[8])))
		mpl.colorbar.ColorbarBase(ax=plt.axes([0.92, 0.1, 0.01, 0.8]),\
			cmap=cmap,norm=norm)
		return fig

	def point(self, lat, lon, string = False):
		j = int(lon+179.5)
		i = int(89.5-lat)
		if string == True:
			fmt = '{0:12.3f} {1:10.3f} {2:10.3f} {3:10.3f}\n'
			strr = '{0:34}={1:10.3f}\n'.format(\
				'Surface elevation',self.data['Bounds'][i,j,0])
			strr = strr + '{0:>12s} {1:>10s} {2:>10s} {3:>10s}\n'.format(\
				'Bottom Dpt.','Vp','Vs','Density')
			for k in range(1,9):
				strr = strr + fmt.format(\
					self.data['Bounds'][i,j][k],\
					self.data['Vp'][i,j][k-1],\
					self.data['Vs'][i,j][k-1],\
					self.data['Rho'][i,j][k-1])
			strr = strr + '{0:12s} {1:10.3f} {2:10.3f} {3:10.3f}\n'.format(\
				'Mantle',self.data['Vp'][i,j,-1],self.data['Vs'][i,j,-1],self.data['Rho'][i,j,-1])
			return strr
		else:
			return self.data['Bounds'][i,j,:],self.data['Vp'][i,j,:],self.data['Vs'][i,j,:],self.data['Rho'][i,j,:]

def read_db(dir='./data/'):
	VpID = open(dir+'crust1.vp','r')
	VsID = open(dir+'crust1.vs','r')
	RhID = open(dir+'crust1.rho','r')
	BdID = open(dir+'crust1.bnds', 'r')
	CRUST1p0 = {'gridDataLat':np.zeros([180,360]),\
				'gridDataLon':np.zeros([180,360]),\
				'Vp':np.zeros([180,360,9]),\
				'Vs':np.zeros([180,360,9]),\
				'Bounds':np.zeros([180,360,9]),\
				'Rho':np.zeros([180,360,9])}
	for i in range(180):
		lat = 89.0 - i + 0.5
		for j in range(360):
			lon = -179 + j -0.5
			CRUST1p0['gridDataLat'][i,j] = lat
			CRUST1p0['gridDataLon'][i,j] = lon
			CRUST1p0['Vp'][i,j,:] = np.array([float(val) for val in VpID.readline().strip().split()])
			CRUST1p0['Vs'][i,j,:] = np.array([float(val) for val in VsID.readline().strip().split()])
			CRUST1p0['Rho'][i,j,:] = np.array([float(val) for val in RhID.readline().strip().split()])
			CRUST1p0['Bounds'][i,j,:] = np.array([float(val) for val in BdID.readline().strip().split()])
	VpID.close()
	VsID.close()
	RhID.close()
	BdID.close()
	pickle.dump(CRUST1p0,open('crust1p0.pkl', 'wb'))
if __name__ == '__main__':
	if not(os.path.isfile('crust1p0.pkl')):
		read_db()
	c = Crust1p0()
	fig, ax = plt.subplots()
	c.plot_crust_at_point(ax,73.5,23.5)
	plt.show()