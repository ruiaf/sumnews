jQuery(document).ready(function($){

    function graph_drawer(element_id) {
        this.settings = {
            "node_radius": 10,
            "node_mass": 10,
            "gravity_attraction": 1,
            "gravity_repulsion": 10,
            "interval": 0.1
        }


        this.canvas = document.getElementById(element_id);
        this.ctx = this.canvas.getContext("2d");
        this.center = {"x": this.canvas.clientHeight/2, "y": this.canvas.clientWidth/2}

        this.nodes = {}
        this.edges = {}

        this.add_node = function(u) {
            u._a = {"x": 0, "y":0};
            u._m = this.settings.node_mass;
            u.x = Math.max(u.x + this.center.x, -this.center.x );
            u.y = Math.max(u.y + this.center.y, -this.center.y );
            u.x = Math.min(u.x - this.center.x, this.center.x );
            u.y = Math.min(u.y - this.center.y, this.center.y );
            this.nodes[u.id] = u;
        }

        this.add_edge = function(e) {
            this.edges[e.id] = e;
        }

        this.draw_node = function(u) {
            this.ctx.beginPath();
            this.ctx.arc(this.center.x + u.x, this.center.y + u.y, this.settings.node_radius, 0, 2*Math.PI);
            this.ctx.fill();
        }

        this.draw_edge = function(e) {

            var u = this.nodes[e.source];
            var v = this.nodes[e.target];

            this.ctx.moveTo(this.center.x + u.x, this.center.y + u.y);
            this.ctx.lineTo(this.center.x + v.x, this.center.y + v.y);
            this.ctx.stroke();
        }

        this.distance = function(u, v) {
            return Math.sqrt((u.x - v.x)*(u.x - v.x) + (u.y - v.y)*(u.y - v.y));
        }

        this.draw = function() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            for (var node in this.nodes) {
                this.draw_node(this.nodes[node]);
            }

            for (var edge in this.edges) {
                this.draw_edge(this.edges[edge]);
            }
        }

        this.repulsion = function() {
            for (var u_id in this.nodes) {
                for (var v_id in this.nodes) {
                    if (u_id==v_id) {
                        continue;
                    }
                    var u = this.nodes[u_id];
                    var v = this.nodes[v_id];

                    var force = this.settings.gravity_repulsion * u._m * v._m / Math.pow( this.distance(u, v), 2);
                    var force_x = force * (v.x - u.x)/Math.abs(v.x - u.x);
                    var force_y = force * (v.y - u.y)/Math.abs(v.y - u.y);

                    u._a.x -= force_x * this.settings.interval / this.settings.node_mass;
                    u._a.y -= force_y * this.settings.interval / this.settings.node_mass;


                    if (this.distance(u, v) <= this.settings.node_radius*2) {
                        u._a = {"x": 0, "y":0};
                    }
                }
            }
        }

        this.attraction = function() {
            for (var e_id in this.edges) {
                var u = this.nodes[this.edges[e_id].source];
                var v = this.nodes[this.edges[e_id].target];

                var force = this.settings.gravity_attraction * u._m * v._m / this.distance(u, v);
                var force_x = force * (v.x - u.x)/Math.abs(v.x - u.x);
                var force_y = force * (v.y - u.y)/Math.abs(v.y - u.y);

                u._a.x += force_x * this.settings.interval / this.settings.node_mass;
                u._a.y += force_y * this.settings.interval / this.settings.node_mass;
                v._a.x -= force_x * this.settings.interval / this.settings.node_mass;
                v._a.y -= force_y * this.settings.interval / this.settings.node_mass;

                if (this.distance(u, v) <= this.settings.node_radius*2) {
                    u._a = {"x": 0, "y":0};
                    v._a = {"x": 0, "y":0};
                }
            }
        }

        this.update_position = function() {
            for (var u_id in this.nodes) {

                u = this.nodes[u_id];

                u.x = u.x + u._a.x * this.settings.interval;
                u.y = u.y + u._a.y * this.settings.interval;
            }
        }

        this.iterate = function() {
            this.draw();
            this.attraction();
            this.repulsion();
            this.update_position();
        }
    }

    var gd = new graph_drawer("cluster_graph");
    gd.add_node({ "id":"node1", "x":0, "y": 0 });
    gd.add_node({ "id":"node2", "x":100, "y": 100 });
    gd.add_edge({ "id":"arc1", "source":"node1", "target": "node2" });

    setInterval(function() { gd.iterate() }, 10);
});