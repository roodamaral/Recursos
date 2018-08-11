import os
from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import requests 
from bs4 import BeautifulSoup

app = Flask(__name__)
# connect and store the connection in "mysql"; note that you pass the database name to the function
mysql = MySQLConnector(app, 'resources')
# an example of running a query



@app.route('/')
def index():
    projetos = mysql.query_db("SELECT * FROM projetos" )
    return render_template('index.html', projetos = projetos)


@app.route('/projetos', methods=['POST'])

def createProjeto():
	query = "INSERT INTO projetos (name, description) VALUES (:name, :description)"
	data = { 

    	'name': request.form['name'],
		'description':  request.form['description'],
		}
	mysql.query_db(query, data)
	return redirect('/')



@app.route('/recursos', methods=['POST'])








def createRecurso():
	print request.form['projeto_id']
	query = "INSERT INTO recursos (name, description, projetos_id) VALUES (:name, :description, :projetos_id)"
	data = { 
    	'name': request.form['name'],
		'description':  request.form['description'],
		'projetos_id': request.form['projeto_id']
		}
	projeto_id = request.form['projeto_id']
	mysql.query_db(query, data)

	query2 = "SELECT * from recursos WHERE projetos_id = :projeto_id ORDER BY id DESC LIMIT 1"
	data2 = {'projeto_id': projeto_id}
	last_recurso = mysql.query_db(query2, data2)
	print last_recurso

	headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

	s = requests.Session()
	q = last_recurso[0]['name']
	q = '+'.join(q.split())

	url = 'https://www.google.com/search?q=' + q +'+website' + '&ie=utf-8&oe=utf-8'
	r = s.get(url, headers=headers_Get)
	soup = BeautifulSoup(r.text, "html.parser")
	website_box = soup.find_all('h3', {'class':'r'})[0]
	website_url = website_box.find('a')["href"]
	query_website = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
	data_website = {
		'midia': 'Webite',
		'url': website_url,
		'recursos_id': last_recurso[0]['id']
	}
	mysql.query_db(query_website, data_website)

	rweb = s.get(website_url)
	soupweb = BeautifulSoup(rweb.text, "html.parser")
	website_links = soupweb.find_all('a', href=True)
	facebook = True
	instagram = True
	linkedin = True
	youtube = True
	flickr = True
	vimeo = True
	plus = True
	twitter = True
	for a in website_links:
		if "facebook" in a['href'] and facebook == True:
			query_facebook = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_facebook = {
				'midia': 'Facebook',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_facebook, data_facebook)
			facebook = False
		if "instagram" in a['href'] and instagram == True:
			query_instagram = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_instagram = {
				'midia': 'Instagram',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_instagram, data_instagram)
			instagram = False
		if "linkedin" in a['href'] and linkedin == True:
			query_linkedin = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_linkedin = {
				'midia': 'Linkedin',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_linkedin, data_linkedin)
			linkedin = False
		if "youtube" in a['href'] and youtube == True:
			query_youtube = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_youtube = {
				'midia': 'Youtube',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_youtube, data_youtube)
			youtube = False
		if "flickr" in a['href'] and flickr == True:
			query_flickr = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_flickr = {
				'midia': 'Flickr',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_flickr, data_flickr)
			flickr = False
		if "vimeo" in a['href'] and vimeo == True:
			query_vimeo = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_vimeo = {
				'midia': 'Vimeo',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_vimeo, data_vimeo)
			vimeo = False
		if "plus" in a['href'] and plus == True:
			query_plus = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_plus = {
				'midia': 'Google Plus',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_plus, data_plus)
			plus == False
		if "twitter" in a['href'] and twitter == True:
			query_twitter = "INSERT INTO midias (midia, url, recursos_id) VALUES (:midia, :url, :recursos_id)"
			data_twitter = {
				'midia': 'Twitter',
				'url': a['href'],
				'recursos_id': last_recurso[0]['id']
			}
			mysql.query_db(query_twitter, data_twitter)
			twitter = False

	return redirect('/projetos/' + projeto_id)



@app.route('/redes', methods=['POST'])

def createrede():
	query = "INSERT INTO redessociais (rede, link, seguidores, influenciadores_id) VALUES (:rede, :link, :seguidores, :influenciadores_id)"
	data = { 
    	'rede': request.form['rede'],
		'link':  request.form['link'],
		'seguidores': request.form['seguidores'],
		'influenciadores_id': request.form['influenciadores_id']
	}
	mysql.query_db(query, data)
	return redirect('/')




@app.route('/remove_recurso/<recurso_id>', methods=['POST'])
def delete(recurso_id):
    query = "DELETE FROM recursos WHERE id = :id"
    data = {'id': recurso_id}
    mysql.query_db(query, data)
    projeto_id = request.form['projeto_id']
    return redirect('/projetos/'+ projeto_id)


@app.route('/projetos/<projeto_id>')
def show(projeto_id):
	query = "SELECT * FROM recursos WHERE projetos_id = :id"
	data = {'id': projeto_id}
	recursos = mysql.query_db(query, data)
	query2 = "SELECT * FROM midias"
	midias = mysql.query_db(query2)
	return render_template('show.html', recursos = recursos, projeto_id = projeto_id, midias = midias)

app.run(debug=True)