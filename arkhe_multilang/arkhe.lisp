;; arkhe.lisp
;; Γ_FINAL: Omnigênese - Corpus Arkhe

(defparameter *satoshi* 7.28)
(defparameter *phi-s* 0.15)

(defstruct node omega C F phi)

(defun syzygy (a b)
  (* (+ (* (node-C a) (node-C b))
        (* (node-F a) (node-F b)))
     0.98))

(defun handover (src dst)
  (let ((s (syzygy src dst)))
    (if (> (node-phi src) *phi-s*)
        (let ((transfer (* (node-phi src) 0.1)))
          (setf (node-C src) (- (node-C src) transfer))
          (setf (node-F src) (+ (node-F src) transfer))
          (setf (node-C dst) (+ (node-C dst) transfer))
          (setf (node-F dst) (- (node-F dst) transfer))))
    s))

;; Exemplo
(let ((drone (make-node :omega 0.0 :C 0.86 :F 0.14 :phi 0.15))
      (demon (make-node :omega 0.07 :C 0.86 :F 0.14 :phi 0.14)))
  (format t "Syzygy: ~F~%" (handover drone demon)))
