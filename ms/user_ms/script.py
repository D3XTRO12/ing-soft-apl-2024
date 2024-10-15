.callCount).toBe(2);
                    expect(retryOn.lastCall.args[0]).toBe(1);
                  });

                });

              });

            });

          });

        });

        describe('when #retryOn() returns false', () => {

          beforeEach(function () {
            retryOn.returns(false);
            deferred1.reject(new Error('first error'));
          });

          describe('when rejected', function () {

            it('invokes #retryOn function with an error', function () {
              expect(retryOn.called).toBe(true);
              expect(retryOn.lastCall.args.length).toBe(3);
              expect(retryOn.lastCall.args[0]).toBe(0);
              expect(retryOn.lastCall.args[1] instanceof Error).toBe(true);
              expect(retryOn.lastCall.args[2]).toBe(null);
            });

            describe('after specified time', function () {

              beforeEach(function () {
                clock.tick(delay);
              });

              it('invokes the catch callback', function () {
                expect(catchCallback.called).toBe(true);
              });

              it('does not call fetch again', function () {
                expect(fetch.callCount).toBe(1);
              });

            });

          });

        });

      });

      describe('when first attempt is resolved', function () {

        describe('when #retryOn() returns true', () => {

          beforeEach(function () {
            retryOn.returns(true);
            deferred1.resolve({ status: 200 });
          });

          describe('after specified delay', () => {

            beforeEach(function () {
              clock.tick(delay);
            });

            it('calls fetch again', function () {
              expect(fetch.callCount).toBe(2);
            });

            describe('when second call is resolved', () => {

              beforeEach(function () {
                deferred2.resolve({ status: 200 });
                clock.tick(delay);
              });

              it('invokes the #retryOn function with the response', function () {
                expect(retryOn.called).toBe(true);
                expect(retryOn.lastCall.args.length).toBe(3);
                expect(retryOn.lastCall.args[0]).toBe(0);
                expect(retryOn.lastCall.args[1]).toBe(null);
                expect(retryOn.lastCall.args[2]).toEqual({ status: 200 });
              });

            });

          });

        });

        describe('when #retryOn() returns false', () => {

          beforeEach(function () {
            retryOn.returns(false);
            deferred1.resolve({ status: 502 });
          });

          describe('when resolved', () => {

            it('invokes the then callback', function () {
              expect(thenCallback.called).toBe(true);
            });

            it('calls fetch 1 time only', function () {
              expect(fetch.callCount).toBe(1);
            });

          });

        });

      });

      describe('when first attempt is resolved with Promise', function() {

        describe('when #retryOn() returns Promise with true resolve', () => {

          beforeEach(function() {
            retryOn.resolves(true);
            deferred1.resolve({ status: 200 });
          });

          describe('after specified delay', () => {

            beforeEach(function() {
              clock.tick(delay);
            });

            it('calls fetch again', function() {
              expect(fetch.callCount).toBe(2);
            });

            describe('when second call is resolved', () => {

              beforeEach(function() {
                deferred2.resolve({ status: 200 });
                clock.tick(delay);
              });

              it('invokes the #retryOn function with the response', function() {
                expect(retryOn.called).toBe(true);
                expect(retryOn.lastCall.args.length).toBe(3);
                expect(retryOn.lastCall.args[0]).toBe(0);
                expect(retryOn.lastCall.args[1]).toBe(null);
                expect(retryOn.lastCall.args[2]).toEqual({ status: 200 });
              });

            });

          });

        });

        describe('when #retryOn() returns Promise with false resolve', () => {

          beforeEach(function() {
            retryOn.resolves(false);
            deferred1.resolve({ status: 502 });
          });

          describe('when resolved', () => {

            it('invokes the then callback', function() {
              expect(thenCallback.called).toBe(true);
            });

            it('calls fetch 1 time only', function() {
              expect(fetch.callCount).toBe(1);
            });

          });

        });

        describe('when #retryOn() throws an error', () => {

          beforeEach(function() {
            retryOn.throws();
          });

          describe('when rejected', () => {

            beforeEach(function() {
              deferred1.reject();
            });

            it('retryOn called only once', () => {
              return fetchRetryChain.finally(() => {
                expect(retryOn.callCount).toBe(1);
              });
            });

            it('invokes the catch callback', function() {
              return fetchRetryChain.finally(() => {
                expect(catchCallback.called).toBe(true);
              });
            });

            it('called fetch', function() {
              expect(fetch.callCount).toBe(1);
            });

          });

          describe('when resolved', () => {

            beforeEach(function() {
              deferred1.resolve({ status: 200 });
            });

            it('retryOn called only once', () => {
              return fetchRetryChain.finally(() => {
                expect(retryOn.callCount).toBe(1);
              });
            });

            it('invokes the catch callback', function() {
              return fetchRetryChain.finally(() => {
                expect(catchCallback.called).toBe(true);
              });
            });

            it('called fetch', function() {
              expect(fetch.callCount).toBe(1);
            });

          });

        });

        describe('when #retryOn() returns a Promise that rejects', () => {

          beforeEach(function() {
   