package sdk

import (
	"fmt"
	"time"
)

type Dec float64

func (d Dec) GT(other Dec) bool { return d > other }
func (d Dec) GTE(other Dec) bool { return d >= other }
func (d Dec) LT(other Dec) bool { return d < other }
func (d Dec) IsZero() bool { return d == 0 }
func (d Dec) String() string { return fmt.Sprintf("%.4f", d) }
func (d Dec) Add(other Dec) Dec { return d + other }
func (d Dec) Sub(other Dec) Dec { return d - other }
func (d Dec) Mul(other Dec) Dec { return d * other }
func (d Dec) Quo(other Dec) Dec { return d / other }
func (d Dec) Abs() Dec {
	if d < 0 {
		return -d
	}
	return d
}

func ZeroDec() Dec { return 0.0 }
func NewDec(i int64) Dec { return Dec(float64(i)) }
func NewDecWithPrec(i int64, prec int64) Dec {
	res := float64(i)
	for j := int64(0); j < prec; j++ {
		res /= 10
	}
	return Dec(res)
}
func MinDec(a, b Dec) Dec {
	if a < b {
		return a
	}
	return b
}

type Context struct {
	blockHeight int64
	blockTime   time.Time
	proposer    string
	eventManager *EventManager
}

func (ctx Context) BlockHeight() int64 { return ctx.blockHeight }
func (ctx Context) BlockTime() time.Time { return ctx.blockTime }
func (ctx Context) BlockHeader() Header { return Header{ProposerAddress: Address(ctx.proposer)} }
func (ctx Context) EventManager() *EventManager {
	if ctx.eventManager == nil {
		return &EventManager{}
	}
	return ctx.eventManager
}

type Header struct {
	ProposerAddress Address
}

type Address string
func (a Address) String() string { return string(a) }

type Coins string // Simplified

type Event struct {
	Type       string
	Attributes []Attribute
}

type Attribute struct {
	Key   string
	Value string
}

func NewEvent(t string, attrs ...Attribute) Event {
	return Event{Type: t, Attributes: attrs}
}

func NewAttribute(k, v string) Attribute {
	return Attribute{Key: k, Value: v}
}

type EventManager struct{}
func (em *EventManager) EmitEvent(e Event) {}

type GovernanceProposal struct {
	Title       string
	Description string
	InstanceID  string
	Deposit     Coins
}
